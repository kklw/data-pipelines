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
    truncate_sql = """
        TRUNCATE TABLE {table}
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
        self.sql = self.sql.format(table=self.table, select_sql=select_sql)
        self.truncate_sql = self.truncate_sql.format(table=self.table)

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_conn_id)
        if not self.append_insert:
            redshift_hook.run(self.truncate_sql)
        redshift_hook.run(self.sql)
