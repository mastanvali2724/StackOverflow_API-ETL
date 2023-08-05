# StackOverflow_API-ETL
* This project aims to develop a robust data collection pipeline using Python to access Stack Overflow's API and retrieve relevant tag, question, and answer data.
* Leveraged airflow to design a sophisticated workflow automation system that enabled seamless scheduling and execution of the data collection process.
* Employed AWS Redshift, a powerful data warehousing solution, to efficiently store and organize the extracted data. This optimized storage for subsequent analysis.
* Successfully gathered trending tag informa tion, user-generated questions, and community-authored answers from Stack Overflow's vast repository of knowledge.
* Created an accessible and structured data source that empowers data analysts and data scientists to perform in-depth analysis and derive actionable insights.
# Architecture
![arch_diagram](./Images/architecture.png)
Architecture of fetching data from Stackoverflow API and loading into Amazon Redshift.

# Business Queries
* Top 3 all-time trending tags.
* Top 3 questions of all-time trending tags in last 30 days.
* Top 3 answers of each question above.

# Screenshots of DAG and Redshift tables.

* Structure of DAG and it's tasks
  
![dag_diagram](./Images/dag2.png)

* Tags table schema
  
![tags_schema](./Images/tags_schema.png)

* Tags Table
  
![tags_table](./Images/tags_table.png)

* Questions table schema
  
![questions_schema](./Images/questions_schema.png)

* Questions Table
  
![questions_table](./Images/questions_table.png)

* Answers table schema
  
![answers_schema](./Images/answers_schema.png)

* Answers Table
  
![answers_table](./Images/answers_table.png)


* Note: Make sure to create the .env file and store the environment variables related to Redshift connection like Hostname, database, user credentials,port number.
