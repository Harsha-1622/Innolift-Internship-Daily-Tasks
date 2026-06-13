# ==========================================
# IMPORTS
# ==========================================

import sqlite3

# ==========================================
# CONNECT DATABASE
# ==========================================

connection = sqlite3.connect(
    "database.db"
)

cursor = connection.cursor()

# ==========================================
# USERS TABLE
# ==========================================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """
)

# ==========================================
# PREDICTIONS TABLE
# ==========================================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS predictions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        global_reactive_power REAL,

        voltage REAL,

        global_intensity REAL,

        sub_metering_1 REAL,

        sub_metering_2 REAL,

        sub_metering_3 REAL,

        predicted_power REAL,

        category TEXT,

        advice TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)

        REFERENCES users(id)

    )
    """
)

# ==========================================
# SAVE CHANGES
# ==========================================

connection.commit()

# ==========================================
# CLOSE DATABASE
# ==========================================

connection.close()

print(
    "Database created successfully!"
)