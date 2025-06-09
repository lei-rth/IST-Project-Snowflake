import snowflake.connector
from dotenv import load_dotenv
from get_data import get_data
import os
import pandas as pd

load_dotenv()

def create_table_if_not_exists():
    df = pd.read_csv('data/flight_data.csv')

    # Map pandas dtypes to Snowflake types
    dtype_mapping = {
        'object': 'STRING',
        'float64': 'FLOAT',
        'int64': 'BIGINT',
        'bool': 'BOOLEAN'
    }

    columns = []
    for col, dtype in zip(df.columns, df.dtypes):
        snowflake_type = dtype_mapping.get(str(dtype), 'STRING')
        columns.append(f'"{col}" {snowflake_type}')

    columns_sql = ",\n  ".join(columns)
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS flight_data (
        {columns_sql}
    );
    """
    return create_table_sql

def upload_data_to_snowflake(data):
    SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
    SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
    SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
    SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE')
    SNOWFLAKE_SCHEMA = os.getenv('SNOWFLAKE_SCHEMA')
    SNOWFLAKE_STAGE = os.getenv('SNOWFLAKE_STAGE')

    try:
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA
        )
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute(create_table_if_not_exists())

        # Upload the dataset to Snowflake
        put_command = f"PUT file://data/flight_data.csv @{SNOWFLAKE_STAGE} OVERWRITE = TRUE;"
        cursor.execute(put_command)
        print(f"Data uploaded to stage: {SNOWFLAKE_STAGE}")

        # Load into table
        copy_command = f"""
        COPY INTO {SNOWFLAKE_SCHEMA}.flight_data
        FROM @{SNOWFLAKE_STAGE}/flight_data.csv
        FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1)
        ON_ERROR = 'CONTINUE';
        """

        cursor.execute(copy_command)
        print(f"Data copied into table: {SNOWFLAKE_SCHEMA}.flight_data")

        conn.commit()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        cursor.close()
        conn.close()
        print("Snowflake connection closed.")

if __name__ == "__main__":
    data = get_data()
    upload_data_to_snowflake(data)
