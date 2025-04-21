import pandas as pd
import pymysql  # For MySQL. Use psycopg2 for PostgreSQL.
import logging
import sys

# Configure logging
logging.basicConfig(
    filename='../logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_csv_to_db(csv_path, db_config):
    try:
        # Load CSV
        logging.info("Loading CSV file: %s", csv_path)
        data = pd.read_csv(csv_path)
        logging.info("CSV loaded successfully with %d records", len(data))

        # Connect to database
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        logging.info("Connected to the database")

        # Insert data
        cursor = connection.cursor()
        for _, row in data.iterrows():
            cursor.execute("""
                INSERT INTO users (id, name, email)
                VALUES (%s, %s, %s)
            """, (row['id'], row['name'], row['email']))
        connection.commit()
        logging.info("Data inserted successfully")

    except Exception as e:
        logging.error("An error occurred: %s", e)
        sys.exit(1)
    finally:
        if connection:
            connection.close()
            logging.info("Database connection closed")