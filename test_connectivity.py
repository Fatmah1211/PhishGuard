import pyodbc
import requests
from config import CONNECTION_STRING, VT_API_KEY, GEMINI_API_KEY

print("\n========== PhishGuard Connectivity Test ==========\n")

try:
    conn = pyodbc.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ScanRequests")
    count = cursor.fetchone()[0]
    conn.close()
    print(f"✅ Database Connected — ScanRequests rows: {count}")
except Exception as e:
    print(f"❌ Database Failed: {e}")

try:
    headers = {"x-apikey": VT_API_KEY}
    r = requests.get("https://www.virustotal.com/api/v3/urls", headers=headers)
    if r.status_code in [200, 400, 405]:
        print("✅ VirusTotal API Connected")
    else:
        print(f"❌ VirusTotal Failed: {r.status_code}")
except Exception as e:
    print(f"❌ VirusTotal Failed: {e}")

if GEMINI_API_KEY:
    print(f"✅ Gemini API Key Configured — Key: {GEMINI_API_KEY[:8]}...")
else:
    print("❌ Gemini API Key Missing")

try:
    r = requests.get("http://127.0.0.1:5000")
    if r.status_code == 200:
        print("✅ Flask Frontend Running — Homepage reachable")
    else:
        print(f"❌ Flask Failed: {r.status_code}")
except Exception as e:
    print(f"❌ Flask Failed: {e}")

print("\n===================================================\n")
