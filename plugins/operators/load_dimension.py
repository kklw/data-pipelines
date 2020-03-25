from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class LoadDimensionOperator(BaseOperator):
    """
    Loads dimension table.
    """

    ui_color = '#80BD9E'
    sql = """
        INSERT INTO {table}
        {select_sql};
    """

    @apply_defaults
    def __init__(self,
                 table,
                 redshift_conn_id='redshift',
                 select_sql='',
                 *args, **kwargs):
        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.select_sql = select_sql

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_conn_id)
        self.sql = self.sql.format(table=self.table, select_sql=self.select_sql)
        redshift_hook.run(self.sql)
