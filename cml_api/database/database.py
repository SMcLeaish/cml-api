import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_user = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_url = f"postgresql://{db_user}:{db_password}@postgresserver/db"
# Delete SQLALCHEMY_DATABASE_URL and change all instances to db_url to switch to
# postgresql, think there is a pg driver also
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
"""
    The argument:

connect_args={"check_same_thread": False}

...is needed only for SQLite. It's not needed for other databases.
"""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
