import snowflake.connector
from dotenv import load_dotenv
from get_data import get_all_data, get_flights_from_zurich
import os
import pandas as pd

load_dotenv()

def create_table_if_not_exists(table_name, file_path):
    df = pd.read_csv(file_path)

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
    CREATE TABLE IF NOT EXISTS {table_name} (
        {columns_sql}
    );
    """
    return create_table_sql

def load_into_table(cursor, table_name, file_path, stage_name):
    file_name = os.path.basename(file_path)

    # Upload the file to the Snowflake stage
    put_command = f"PUT file://{file_path} @{stage_name} OVERWRITE = TRUE;"
    cursor.execute(put_command)

    # Load data into the table
    copy_command = f"""
    COPY INTO {table_name}
    FROM @{stage_name}/{file_name}
    FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1)
    ON_ERROR = 'CONTINUE';
    """
    cursor.execute(copy_command)

def upload_data_to_snowflake():
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

        # Create the table that contains the flight data if it doesn't exist
        flight_data_table_name = 'flight_data'
        cursor.execute(create_table_if_not_exists(flight_data_table_name, 'data/flight_data.csv'))

        # Create the table that contains the flights from Zurich if it doesn't exist
        flights_from_zurich_table_name = 'flights_from_zurich'
        cursor.execute(create_table_if_not_exists(flights_from_zurich_table_name, 'data/flights_from_zurich.csv'))

        # Upload the dataset to Snowflake
        flight_data_put_command = f"PUT file://data/flight_data.csv @{SNOWFLAKE_STAGE} OVERWRITE = TRUE;"
        cursor.execute(flight_data_put_command)
        print(f"Flight data uploaded to stage: {SNOWFLAKE_STAGE}")

        # Upload the flights from Zurich dataset to Snowflake
        flights_from_zurich_put_command = f"PUT file://data/flights_from_zurich.csv @{SNOWFLAKE_STAGE} OVERWRITE = TRUE;"
        cursor.execute(flights_from_zurich_put_command)
        print(f"Flights from Zurich data uploaded to stage: {SNOWFLAKE_STAGE}")

        # Load into table
        load_into_table(cursor, f"{SNOWFLAKE_SCHEMA}.{flight_data_table_name}", 'data/flight_data.csv', SNOWFLAKE_STAGE)
        print(f"Flight data copied into table: {SNOWFLAKE_SCHEMA}.{flight_data_table_name}")

        # Load flights from Zurich into table
        load_into_table(cursor, f"{SNOWFLAKE_SCHEMA}.{flights_from_zurich_table_name}", 'data/flights_from_zurich.csv', SNOWFLAKE_STAGE)
        print(f"Flights from Zurich data copied into table: {SNOWFLAKE_SCHEMA}.{flights_from_zurich_table_name}")

        conn.commit()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        cursor.close()
        conn.close()
        print("Snowflake connection closed.")

if __name__ == "__main__":
    get_all_data()
    get_flights_from_zurich()
    upload_data_to_snowflake()
