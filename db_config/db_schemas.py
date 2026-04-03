import datetime
from sqlite3.dbapi2 import Timestamp

from sqlalchemy import Column, String, UniqueConstraint, BigInteger, DateTime, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import now, func

# --- Declarative Base ---
Base = declarative_base()


# ----  User Table  ----
class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("id","phone", name="unique_user_id_phone"),)

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    username = Column(String(255), nullable=False)
    phone = Column(BigInteger,unique=True, nullable=False)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())