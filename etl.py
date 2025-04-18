import pandas as pd
import json
import sqlite3
import os

# Check if file exists
if not os.path.exists("events_log.json"):
    print("❌ events_log.json not found. Please run app.py and send some events first.")
    exit()

# Read the log file into a list of dicts
with open("events_log.json", "r") as f:
    events = [json.loads(line) for line in f if line.strip()]

# Convert to DataFrame
df = pd.DataFrame(events)

# Convert 'data' dict to JSON string so SQLite can store it
if 'data' in df.columns:
    df['data'] = df['data'].apply(json.dumps)

# Save cleaned data as CSV
df.to_csv("cleaned_events.csv", index=False)
print("✅ Saved to cleaned_events.csv")

# Save to SQLite DB
conn = sqlite3.connect("vistora_events.db")
df.to_sql("events", conn, if_exists="replace", index=False)
conn.close()
print("✅ Saved to vistora_events.db")