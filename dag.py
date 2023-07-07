import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta, date
import psycopg2
from popular_tags import fetch_popular_tags
from top_questions_by_tag import fetch_top_questions
from top_answers_by_question import fetch_answers
from dotenv import load_dotenv

load_dotenv()
redshift_host = os.getenv("REDSHIFT_HOSTNAME")
redshift_port = os.getenv("REDSHIFT_PORT")
redshift_db = os.getenv("REDSHIFT_DATABASE")
username = os.getenv("REDSHIFT_USERNAME")
password = os.getenv("REDSHIFT_PASSWORD")
default_args = {
    'start_date': datetime(2023, 7, 5),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'stackoverflow_data_pipeline',
    default_args=default_args, 
    schedule_interval='@once', 
    catchup=False
    )


def store_tags(tags):
    # store the fetched tags in the database
    # query to create a table(if not exists) and insert the tags
    insert_query = "CREATE TABLE IF NOT EXISTS tags (tag_name VARCHAR(50) PRIMARY KEY, tag_count INTEGER, month VARCHAR(7));INSERT INTO tags (tag_name, tag_count, month) VALUES %s"
    previous_month = (date.today().replace(day=1) - timedelta(days=1)).strftime("%Y-%m")
    tag_values = [(tag["name"], tag["count"], previous_month) for tag in tags]
    # Create a Redshift Connection
    redshift_conn = psycopg2.connect(
        host=redshift_host,
        port=redshift_port,
        database=redshift_db,
        user=username,
        password=password
    )
    with redshift_conn:
        with redshift_conn.cursor() as cursor:
            # Execute the query
            psycopg2.extras.execute_values(cursor, insert_query, tag_values)
    # Closing the Redshift connection
    redshift_conn.close()
    print("TAGS STORED")


def store_questions(questions):
    # store the fetched questions in the database
    # Query to create questions table(if not exists) and insert the questions.
    insert_query = "CREATE TABLE IF NOT EXISTS questions (question_id INTEGER PRIMARY KEY , title VARCHAR(1000), view_count integer, creation_date TIMESTAMP, score INTEGER, link VARCHAR(1000), answer_count INTEGER, last_activity_date TIMESTAMP, is_answered BOOLEAN);INSERT INTO questions (question_id, title, view_count, creation_date, score, link, answer_count, last_activity_date, is_answered) VALUES %s"
    question_values = [(q["question_id"], q["title"], q["view_count"], datetime.utcfromtimestamp(int(q["creation_date"])).strftime('%Y-%m-%d %H:%M:%S'), q["score"], q["link"],q["answer_count"],datetime.utcfromtimestamp(int(q["last_activity_date"])).strftime('%Y-%m-%d %H:%M:%S'), q["is_answered"]) for q in questions]
    redshift_conn = psycopg2.connect(
        host=redshift_host,
        port=redshift_port,
        database=redshift_db,
        user=username,
        password=password
    )
    with redshift_conn:
        with redshift_conn.cursor() as cursor:
            # Executing the query
            psycopg2.extras.execute_values(cursor, insert_query, question_values)

    # Closing the Redshift connection
    redshift_conn.close()
    print("QUESTIONS STORED")

def store_answers(answers):
    # Code to store the fetched answers in the database
    # Query to create answers table(if not exists) and insert the answers.
    insert_query = "CREATE TABLE IF NOT EXISTS answers (answer_id INTEGER PRIMARY KEY, question_id INTEGER, score INTEGER, link VARCHAR(1000),last_activity_date TIMESTAMP, is_accepted BOOLEAN);INSERT INTO answers (answer_id, question_id, score, link, last_activity_date, is_accepted) VALUES %s"
    answer_values = [(a["answer_id"], a["question_id"], a["score"], a["link"], datetime.utcfromtimestamp(int(a["last_activity_date"])).strftime('%Y-%m-%d %H:%M:%S'), a["is_accepted"]) for a in answers]
    redshift_conn = psycopg2.connect(
        host=redshift_host,
        port=redshift_port,
        database=redshift_db,
        user=username,
        password=password
    )
    with redshift_conn:
        with redshift_conn.cursor() as cursor:
            # Executing the query
            psycopg2.extras.execute_values(cursor, insert_query, answer_values)
    # Closing the Redshift connection
    redshift_conn.close()
    print("ANSWERS STORED")

# Defining the tasks
fetch_tags_task = PythonOperator(task_id='fetch_tags', python_callable=fetch_popular_tags, dag=dag)
store_tags_task = PythonOperator(task_id='store_tags', python_callable=store_tags,op_args = [fetch_tags_task.output], dag=dag)
fetch_questions_task = PythonOperator(task_id='fetch_questions', python_callable=fetch_top_questions, op_args = [fetch_tags_task.output], dag=dag)
store_questions_task = PythonOperator(task_id='store_questions', python_callable=store_questions,op_args = [fetch_questions_task.output], dag=dag)
fetch_answers_task = PythonOperator(task_id='fetch_answers', python_callable=fetch_answers,op_args = [fetch_questions_task.output], dag=dag)
store_answers_task = PythonOperator(task_id='store_answers', python_callable=store_answers,op_args = [fetch_answers_task.output], dag=dag)

# Defining the dependencies
fetch_tags_task >> store_tags_task
fetch_tags_task >> fetch_questions_task
fetch_questions_task >> store_questions_task
fetch_questions_task >> fetch_answers_task
fetch_answers_task >> store_answers_task