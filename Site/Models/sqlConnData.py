from sqlalchemy import create_engine
import pandas

class SqlConnection():
    def __init__(self):
        self.ServerName = ""
        self.Database = ""
        self.Driver = ""
        self.ConnectionString = ""
        self.engine = create_engine(self.ConnectionString)

    def GetConnection(self):
        try:
            con = self.engine.connect()
            return con
        except Exception as e:
            print(e)
            return None