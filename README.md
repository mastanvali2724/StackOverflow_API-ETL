# StackOverflow_API-ETL

# Architecture
![arch_diagram](./Images/architecture.png)
Architecture of fetching data from Stackoverflow API and loading into Amazon Redshift.

# Business Queries
* Top 3 all-time trending tags.
* Top 3 questions of all-time trending tags in last 30 days.
* Top 3 answers of each question above.

# Screenshots of DAG and Redshift tables.

![dag_diagram](./Images/dag2.png)

![tags_schema](./Images/tags_schema.png)

![tags_table](./Images/tags_table.png)

![questions_schema](./Images/questions_schema.png)

![questions_table](./Images/questions_table.png)

![answers_schema](./Images/answers_schema.png)

![answers_table](./Images/answers_table.png)
