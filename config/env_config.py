import os

from dotenv import load_dotenv


# --- Loading Env ---
load_dotenv()


# --- Class Config ---
class Config:

    # --- Default Constructor ---
    def __init__(self):
        pass


    # --- Env Variables Func ----
    def get_variable(self, variable_name):
        """get variable from .env"""

        try:
            os.getenv(variable_name)
            return os.getenv(variable_name)

        except Exception as e:
            print(f"exception occurred while accessing env variable: {e} !")