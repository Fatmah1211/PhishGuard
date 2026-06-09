import csv
import pyodbc
from config import CONNECTION_STRING

conn = pyodbc.connect(CONNECTION_STRING)
cursor = conn.cursor()

with open('phishing_urls.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    count = 0
    for row in reader:
        if count >= 2000:
            break
        try:
            cursor.execute("""
                INSERT INTO PhishingDatabase (url, source, is_active, threat_type)
                VALUES (?, ?, ?, ?)
            """, row['url'], 'PhishTank', 1, 'phishing')
            count += 1
        except:
            continue

conn.commit()
conn.close()
print(f"{count} URLs seeded successfully!")
