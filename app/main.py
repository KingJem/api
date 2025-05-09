import os
import pymssql
from fastapi import FastAPI
from loguru import logger

app = FastAPI()

# Configure logging
logger.add("logs/app.log", rotation="500 MB", retention="7 days")

auth = {
    "user": os.getenv('SQL_USER') or 'sa',
    "password": os.getenv('SQL_PASSWORD') or 'YourStrong!Passw0rd',
    "database": os.getenv('SQL_DATABASE') or 'TestDB',
    "host": os.getenv('SQL_HOST') or 'localhost',
    "port": os.getenv('SQL_PORT') or '1433',

}


# Database configuration
def get_db_connection():
    try:
        return pymssql.connect(**auth)
    except pymssql.Error as e:  # 修改异常类型
        logger.error(f"Connection failed: {str(e)}")
        raise


@app.get("/data")
async def get_data():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(as_dict=True)
        cursor.execute("SELECT * FROM testName")
        results = [row for row in cursor.fetchall()]
        return {"databases": results}
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        return {"error": "Database connection failed", "details": str(e)}
    finally:
        if conn:
            conn.close()


# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}
