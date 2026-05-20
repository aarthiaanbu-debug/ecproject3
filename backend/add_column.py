import sqlite3

conn = sqlite3.connect("app.db")

cursor = conn.cursor()

try:

    cursor.execute(
        "ALTER TABLE users ADD COLUMN organization_id INTEGER"
    )

    conn.commit()

    print("organization_id column added successfully")

except Exception as e:

    print("ERROR:", e)

conn.close()