from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class DataQualityOperator(BaseOperator):
    """
    Checks if data have been loaded correctly.
    """
    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='redshift',
                 sql="",
                 expected_result="",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql = sql
        self.expected_result = expected_result

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_conn_id)

        self.log.info("Running test")
        records = redshift_hook.get_records(self.sql)
        actual_result = records[0][0]
        if actual_result != self.expected_result:
            error_message = f"""
                Data quality stage failed.\n
                {actual_result} does not equal {self.expected_result}
            """
            raise AssertionError(error_message)
        else:
            self.log.info("Data quality stage passed")
