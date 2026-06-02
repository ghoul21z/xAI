import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Database")

# Define paths for possible SQLite fallback
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DB_PATH = os.path.join(BASE_DIR, "face_analysis.db")
SQLITE_URL = f"sqlite:///{SQLITE_DB_PATH}"

# Fetch PostgreSQL URL from environment or use a default local database
POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/face_analysis")
if POSTGRES_URL and POSTGRES_URL.startswith("postgres://"):
    POSTGRES_URL = POSTGRES_URL.replace("postgres://", "postgresql://", 1)

# Determine engine based on connection success
engine = None
SessionLocal = None
database_status = "PostgreSQL"
connection_error = None

# Attempt to connect to PostgreSQL
try:
    logger.info(f"Attempting connection to PostgreSQL: {POSTGRES_URL.split('@')[-1]}")
    # Using a small timeout to fail fast if database is down
    engine = create_engine(POSTGRES_URL, connect_args={"connect_timeout": 3})
    # Test connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Successfully connected to PostgreSQL database!")
except Exception as e:
    connection_error = str(e)
    logger.warning(f"Could not connect to PostgreSQL. Error: {e}")
    logger.info(f"Falling back to SQLite database at: {SQLITE_DB_PATH}")
    database_status = "SQLite Fallback"
    
    # Fallback to SQLite
    engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("SQLite session initialized.")

Base = declarative_base()

def get_db():
    """Dependency generator to yield database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_status():
    """Returns the type of database connected and any error messages."""
    return {
        "status": database_status,
        "connected_url": str(engine.url) if engine else None,
        "error": connection_error
    }
