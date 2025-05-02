from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# # Load environment variables from .env file
load_dotenv()

# -------- env load and setup ------

server = os.getenv('SERVER')
database = os.getenv('DATABASE')

# Construct the connection string
SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"

# Create the engine
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()  # Create a new session instance
    try:
        yield db  # Yield the session to be used in the request
    finally:
        db.close()  # Close the session after usage


