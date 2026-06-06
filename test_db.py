import pyodbc
from config import CONNECTION_STRING

try:
    conn = pyodbc.connect(CONNECTION_STRING)
    print("✅ Database connected successfully!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
