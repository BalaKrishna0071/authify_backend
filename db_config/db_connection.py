


from config.env_config import Config
from sqlalchemy import create_engine

# --- Config ---
config = Config()


class DbConnection:

    # --- Default Constructor ---
    def __init__(self):
        self.HOST = config.get_variable("DB_HOST")
        self.USER = config.get_variable("DB_USER")
        self.PASSWORD = config.get_variable("DB_PASSWORD")
        self.DATABASE = config.get_variable("DB_DATABASE")
        self.PORT = config.get_variable("DB_PORT")
        self.engine = create_engine(f"postgresql+psycopg2://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}")


