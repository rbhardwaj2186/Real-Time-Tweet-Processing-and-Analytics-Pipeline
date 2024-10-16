import pyflink
from pyflink.table import TableEnvironment, EnvironmentSettings

import os
os.environ['PYFLINK_CLIENT_JVM_OPTIONS'] = "--add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED"


# Create a TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)

t_env.get_config().get_configuration().set_string(
    "pipeline.jars",
    "file:///E:/Projects/TTV/TRS/KafkaTwitter/jars/flink-sql-connector-kafka_2.11-1.14.4.jar"
)


# Define source table DDL
source_ddl = """
    CREATE TABLE source_table(
        id_str VARCHAR,
        username VARCHAR,
        tweet VARCHAR,
        location VARCHAR,
        retweet_count BIGINT,
        followers_count BIGINT,
        lang VARCHAR
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'my-topic-test',
        'properties.bootstrap.servers' = 'localhost:9092',
        'properties.group.id' = 'test_3',
        'scan.startup.mode' = 'latest-offset',
        'format' = 'json'
    )
"""

# Execute DDL statement to create the source table
t_env.execute_sql(source_ddl)

# Retrieve the source table
source_table = t_env.from_path('source_table')

print("Source Table Schema:")
source_table.print_schema()

# Define a SQL query to select all columns from the source table
sql_query = "SELECT * FROM source_table"

# Execute the query and retrieve the result table
result_table = t_env.sql_query(sql_query)

# Print the result table to the console
result_table.execute().print()
