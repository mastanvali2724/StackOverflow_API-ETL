# StackOverflow_API-ETL

# Architecture
![arch_diagram](./architcture.png)
Architecture of fetching data from Stackoverflow API and loading into Amazon Redshift.

# Business Queries
* Top 3 all-time trending tags.
* Top 3 questions of all-time trending tags in last 30 days.
* Top 3 answers of each question above.

# Screenshots of DAG and Redshift tables.

![dag_diagram](./dag2.png)
![tags_schema](./tags_schema.png)
![tags_table](./tags_table.png)
![questions_schema](./questions_schema.png)
![questions_table](./questions_tabe.png)
![answers_schema](./answers_schema.png)
![answers_table](./answers_table.png)
