import sqlite3

# Connect to the database
conn = sqlite3.connect('billing.db')
cursor = conn.cursor()

# Rename old table temporarily
cursor.execute("ALTER TABLE billing RENAME TO billing_old;")

# Create new billing table with ID
cursor.execute('''
    CREATE TABLE billing (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        amount REAL
    );
''')

# Copy data from old table to new one
cursor.execute('''
    INSERT INTO billing (name, amount)
    SELECT name, amount FROM billing_old;
''')

# Drop the old table
cursor.execute("DROP TABLE billing_old;")

conn.commit()
conn.close()

print("✅ Billing table updated with unique ID column!")