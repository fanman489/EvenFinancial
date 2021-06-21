
import pyarrow.parquet as pq
import psycopg2
from io import StringIO
import csv

def readParquet(directory):
    data_parquet = pq.read_table('..\Data\ds_clicks.parquet.gzip')

    data_pd = data_parquet.to_pandas()

    return data_pd



def connect(params_dic):
    conn = None

    try:
        print("Connecting to PostgreSQL databse")

        conn = psycopg2.connect(**params_dic)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit(1)

    print("Connection successful"
          )
    return conn

"""This function copies the csv data into a table in the sql database"""
def psql_insert_copy(table, conn, keys, data_iter):
    # gets a DBAPI connection that can provide a cursor
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name

        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
            table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)