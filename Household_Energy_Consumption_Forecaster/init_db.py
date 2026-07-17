# ==========================================
# IMPORTS
# ==========================================

import os
import psycopg2
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)
# ==========================================
# DATABASE INITIALIZATION
# ==========================================
def init_db():

    connection = get_connection()
    cursor = connection.cursor()

    # USERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id SERIAL PRIMARY KEY,

            username TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # PREDICTIONS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (

            id SERIAL PRIMARY KEY,

            user_id INTEGER,

            global_reactive_power DOUBLE PRECISION,

            voltage DOUBLE PRECISION,

            global_intensity DOUBLE PRECISION,

            sub_metering_1 DOUBLE PRECISION,

            sub_metering_2 DOUBLE PRECISION,

            sub_metering_3 DOUBLE PRECISION,

            predicted_power DOUBLE PRECISION,

            category TEXT,

            advice TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)

        )
    """)

    connection.commit()
    cursor.close()
    connection.close()

    print("PostgreSQL Database initialized successfully!")