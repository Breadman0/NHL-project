import sqlite3
import pandas as pd

csv_filename = r"C:\Users\pytho\Documents\nhl\merged_og.csv" 
db_filename = "events.db"

print("Starting database conversion... This might take a quick minute.")

conn = sqlite3.connect(db_filename)

chunk_size = 100_000
for chunk in pd.read_csv(csv_filename, chunksize=chunk_size):
    
    chunk["date"] = pd.to_datetime(chunk["date"]).dt.strftime("%Y-%m-%d")

    chunk.to_sql("events", conn, if_exists="append", index=False)

print("Data successfully loaded into database! Creating speed index...")


cursor = conn.cursor()
cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON events (date);")
conn.commit()

conn.close()
print("Success! Your 'events.db' file is ready to power your Streamlit app.")