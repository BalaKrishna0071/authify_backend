from fastapi import HTTPException, status
from sqlalchemy import text

from db_config.db_connection import DbConnection

db = DbConnection()


# --- CRUD Operation Func ---


# ---- Insertion Func ----
def insert_user_details(username: str, email: str, password: str, phone: int):
    """Insert user details into database"""

    try:
        stmt = f"""INSERT INTO users(username, email, password_hash, phone) VALUES(:username, :email, :password_hash, :phone);"""
        with db.engine.connect() as conn:
            conn.execute(text(stmt), parameters={"username": username, "email": email, "password_hash": password, "phone": phone})
            conn.commit()

    except Exception as e:
        print(f"exception occurred while inserting into db: {e} !")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# ---- Fetching Func ----
def fetch_user_details(email: str) -> dict | None:
    """Fetch user details into database"""

    try:
        stmt = f"""SELECT * FROM users WHERE email = :email;"""
        with (db.engine.connect() as conn):
            query_data = conn.execute(text(stmt), parameters={"email": email})
            data = query_data.mappings().fetchone()
            if data:
                return dict(data)
            else:
                return None

    except Exception as e:
        print(f"exception occurred while fetching into db: {e} !")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )




# ---- Updating  Func ----
def update_user_details(email: str, password_hash: str):
    """Update user details into database"""

    try:
        stmt = f"""UPDATE users SET password_hash = :password_hash WHERE email = :email;"""

        with db.engine.connect() as conn:
            conn.execute(text(stmt), parameters={"password_hash": password_hash, "email": email})
            conn.commit()


    except Exception as e:
        print(f"exception occurred while updating into db: {e} !")



# ---- Deletion Func ----
def delete_user_details(email: str):
    """Deleting user details into database"""

    try:
        stmt = f"""DELETE FROM users WHERE email = :email;"""
        with db.engine.connect() as conn:
            conn.execute(text(stmt), parameters={"email": email})
            conn.commit()


    except Exception as e:
        print(f"exception occurred while deleting into db: {e} !")