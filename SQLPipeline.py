
import utils
import pandas as pd
import sqlalchemy



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
                    print("Executed query to create schema: " + query)


    def createTables(self, tables, schema, data_list):
        engine = sqlalchemy.create_engine('postgresql+psycopg2://' + self.parameters["database"] + ':' + self.parameters["password"] + '@localhost/' + self.parameters['user'])

        if len(tables) != len(schema):
            print("table and schema do not match")
            return


        for i in range(len(tables)):

            try:
                data_list[i].to_sql(tables[i], engine, schema=schema[i], method= utils.psql_insert_copy)
            except ValueError as e:
                print(e)

    """select data"""
    def selectData(self, query):
        self.cur.execute(query)
        data = pd.DataFrame(self.cur.fetchall())
        data.columns = [x[0] for x in self.cur.description]

        return data

