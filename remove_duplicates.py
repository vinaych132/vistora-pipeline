import sqlite3

# Connect to the billing database
conn = sqlite3.connect('billing.db')
cursor = conn.cursor()

# Delete duplicate rows based on name + amount, keeping only the first one
cursor.execute('''
    DELETE FROM billing
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM billing
        GROUP BY name, amount
    );
''')

conn.commit()
conn.close()
print("✅ Duplicate entries removed successfully!")