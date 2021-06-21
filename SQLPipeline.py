
import utils
import pandas as pd
import sqlalchemy
import psycopg2
from io import StringIO
import csv


class Pipeline():
    def __init__(self, param_dict):
        self.conn = utils.connect(param_dict)
        self.cur = self.conn.cursor()
        self.parameters = param_dict



    """Creates the schemas in the SQL database from a list of queries"""
    def createSchemas(self, schema_queries):


        # Create Schema and Tables:
        with self.conn:
            with self.conn.cursor() as cursor:

                for query in schema_queries:
                    cursor.execute(query)


    def createTables(self, tables, schema):
        engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:' + self.parameters["password"] + '@localhost/' + self.parameters['user'])

        tables.to_sql(tables, engine, schema=schema, method=utils.psql_insert_copy)


    """select data"""
    def selectData(self, query):
        self.cur.execute(query)
        data = pd.DataFrame(self.cur.fetchall())
        data.columns = [x[0] for x in self.cur.description]

        return data

