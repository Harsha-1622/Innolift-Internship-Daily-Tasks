# ==========================================
# IMPORTS
# ==========================================

import sqlite3

# ==========================================
# CONNECT TO DATABASE
# ==========================================

connection = sqlite3.connect(
    "database.db"
)

cursor = connection.cursor()

# ==========================================
# CREATE TABLE
# ==========================================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS predictions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        global_reactive_power REAL,

        voltage REAL,

        global_intensity REAL,

        sub_metering_1 REAL,

        sub_metering_2 REAL,

        sub_metering_3 REAL,

        predicted_power REAL,

        category TEXT,

        advice TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
)

# ==========================================
# SAVE CHANGES
# ==========================================

connection.commit()

# ==========================================
# CLOSE CONNECTION
# ==========================================

connection.close()

print(
    "Database and predictions table created successfully!"
)