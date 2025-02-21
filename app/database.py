import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

def resource_path(relative_path):
    """Get absolute path for bundled resources when running as an executable."""
    try:
        base_path = sys._MEIPASS2  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Fetch database URL from environment variables
SQLALCHEMY_DATABASE_URL = os.getenv('DB_URL')

# Ensure the database URL is set; otherwise, raise an error
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DB_URL environment variable is not set. Please check your .env file or system environment variables.")

# Fetch admin password from environment variables
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for database session
def get_db():
    """Provide a transactional scope around a series of operations."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
