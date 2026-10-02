import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()


async def get_connection():
    try:
        connection = await asyncpg.connect(
            database = "homework1",
            port= 5432,
            user = "postgres",
            password = os.getenv("DB_PASSWORD"),
            host = "localhost"
        )
        return connection
    except Exception as error:
        print(f"Error with connection: {error}")
        raise


async def create_database():
    connection = None
    try:
        connection = await get_connection()
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                text TEXT NOT NULL
            );
        """)
        print("Table created Successful")
    except Exception as error:
        print(f"Error with create table: {error}")
        raise
    finally:
        if connection:
            await connection.close()