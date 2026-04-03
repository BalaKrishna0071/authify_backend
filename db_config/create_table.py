
from db_config.db_connection import DbConnection
from db_config.db_schemas import Base



# --- DbConnection Instance ----
db_connect = DbConnection()



# ----- Create Table Func ----
def create_table():
    """"""
    if db_connect.engine:
        Base.metadata.create_all(db_connect.engine)
        Base.metadata.create_all(db_connect.engine)
        print(f"Tables created successfully")

    else:
        print(f"Tables not created yet")




if __name__ == '__main__':
    create_table()