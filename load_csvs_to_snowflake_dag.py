from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeQueryOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='load_csvs_to_snowflake_tables_v2',  # NEW DAG ID!
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    description='Load cleaned CSVs into Snowflake with FORCE=TRUE',
) as dag:

    load_uci_credit_default = SnowflakeQueryOperator(
        task_id='load_uci_credit_default_cleaned',
        snowflake_conn_id='snowflake_conn',
        sql="""
            COPY INTO FINANCE_PROJECT.ANALYTICS.UCI_CREDIT_DEFAULT
            FROM @FINANCE_PROJECT.ANALYTICS.MY_STAGE/uci_credit_default_cleaned.csv
            FILE_FORMAT = (TYPE = 'CSV', FIELD_OPTIONALLY_ENCLOSED_BY='"', SKIP_HEADER=1)
            FORCE = TRUE;
        """,
    )

    load_bank_customer_churn = SnowflakeQueryOperator(
        task_id='load_bank_customer_churn_cleaned',
        snowflake_conn_id='snowflake_conn',
        sql="""
            COPY INTO FINANCE_PROJECT.ANALYTICS.BANK_CUSTOMER_CHURN
            FROM @FINANCE_PROJECT.ANALYTICS.MY_STAGE/bank_customer_churn_cleaned.csv
            FILE_FORMAT = (TYPE = 'CSV', FIELD_OPTIONALLY_ENCLOSED_BY='"', SKIP_HEADER=1)
            FORCE = TRUE;
        """,
    )

    load_personal_loan_modeling = SnowflakeQueryOperator(
        task_id='load_personal_loan_modeling_cleaned',
        snowflake_conn_id='snowflake_conn',
        sql="""
            COPY INTO FINANCE_PROJECT.ANALYTICS.PERSONAL_LOAN_MODELING
            FROM @FINANCE_PROJECT.ANALYTICS.MY_STAGE/personal_loan_modeling_cleaned.csv
            FILE_FORMAT = (TYPE = 'CSV', FIELD_OPTIONALLY_ENCLOSED_BY='"', SKIP_HEADER=1)
            FORCE = TRUE;
        """,
    )

    # Task order
    load_uci_credit_default >> load_bank_customer_churn >> load_personal_loan_modeling
