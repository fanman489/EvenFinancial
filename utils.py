
import pyarrow.parquet as pq
import psycopg2
from io import StringIO
import csv
import matplotlib as plt
import pandas as pd

def readParquet(directory):
    data_parquet = pq.read_table(directory)

    data_pd = data_parquet.to_pandas()

    return data_pd



def connect(params_dic):
    conn = None

    try:
        print("Connecting to PostgreSQL databse")

        conn = psycopg2.connect(**params_dic)

    except (Exception, psycopg2.DatabaseError) as error:
        conn = psycopg2.connect(user = params_dic["user"], password = params_dic["password"], host = params_dic["host"])
        conn.autocommit = True
        try:
            query = "create database " + params_dic["database"]
            cur = conn.cursor()
            cur.execute(query)
        except ValueError as e:
            print(e)
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



def printStats(data, column):
    print("Descriptive Statistics For:", column)
    print("mean:", data[column].mean())
    print("median:", data[column].median())
    print("min:", data[column].min())
    print("max:", data[column].max())


def exploration(data):

    clicked = data[data['clicked_at'] == 1]
    not_clicked = data[data['clicked_at'] == 0]

    printStats(clicked, 'annual_income')
    printStats(not_clicked, 'annual_income')

    printStats(clicked, 'requested')
    printStats(not_clicked, 'requested')

    data.groupby('clicked_at').mean()
    data.groupby('loan_purpose').mean()

    table = pd.crosstab(data.loan_purpose, data.clicked_at)
    table.div(table.sum(1).astype(float), axis=0).plot(kind='bar', stacked=True)

    table = pd.crosstab(data.lender_id, data.clicked_at)
    table.div(table.sum(1).astype(float), axis=0).plot(kind='bar', stacked=True)



    bins_list = [0, 500, 1000, 1500, 5000, 10000]

    plt.title("Count of Leads")
    plt.xlabel("Requested Amount")
    plt.ylabel("Count")
    plt.hist(data['requested'], bins=bins_list);

    res = [sum(1 for ele in data['requested'] if ele >= 20000)]
    printStats(data, 'requested')


