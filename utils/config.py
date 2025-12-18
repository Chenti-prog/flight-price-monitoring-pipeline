import os
from dotenv import load_dotenv

load_dotenv()

def get_pg_config() -> dict:
    """
    Returns PostgreSQL connection configuration loaded from environment variables.
    """
    return {
        "host": os.getenv("PG_HOST", "localhost"),
        "port": int(os.getenv("PG_PORT", "5432")),
        "dbname": os.getenv("PG_DB", "flight_prices_db"),
        "user": os.getenv("PG_USER", "flight_user"),
        "password": os.getenv("PG_PASSWORD", "flight_pass"),
    }
