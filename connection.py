import psycopg2
import logging

POSTGRES_DB = "postgres"
POSTGRES_USER = "admin"
POSTGRES_PASSWORD = "12345678"
POSTGRES_SERVER = "127.0.0.1"
POSTGRES_PORT = "5432"

logger = logging.getLogger(__name__)

async def connect_to_db() -> None:
        try:
            logger.warn("--- DB CONNECTION START ---")
            db =  psycopg2.connect(
                    database = POSTGRES_DB,
                    user = POSTGRES_USER,
                    password = POSTGRES_PASSWORD,
                    host = POSTGRES_SERVER,
                    port = POSTGRES_PORT)
            logger.warn("--- DB CONNECTION SUCCESS ---")
        except Exception as e:
            logger.warn("--- DB CONNECTION ERROR ---")
            logger.warn(e)
            logger.warn("--- DB CONNECTION ERROR ---")
        return db

async def close_db_connection(conn, cursor) -> None:
        try:
            logger.warn("--- DB CLOSE START ---")
            cursor.close()
            conn.close()
            logger.warn("--- DB CLOSE SUCCESS ---")
        except Exception as e:
            logger.warn("--- DB COLOSE ERROR ---")
            logger.warn(e)
            logger.warn("--- DB COLOSE ERROR ---")

    