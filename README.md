# PhishGuard 🛡️
### AI-Powered Phishing Detection & Logging System

PhishGuard is a cybersecurity web application that detects malicious and phishing URLs using real-time threat intelligence. Built by BS Cybersecurity students at the University of Management and Technology (UMT), Lahore.

---

## 🔍 What It Does

- User submits a URL
- App checks it against 90+ security engines via VirusTotal API
- Results are stored in a SQL Server database
- Gemini AI generates a plain English threat summary
- User gets a clear verdict: Clean, Suspicious, or Malicious

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + Flask |
| Database | Microsoft SQL Server (SSMS) |
| Threat Detection | VirusTotal API |
| AI Integration | Google Gemini API |
| Frontend | HTML, CSS, Bootstrap |

---

## 🗄️ Database Collections

- **Users** — Authentication and user management
- **ScanRequests** — Every URL submission log
- **ThreatReports** — Detailed VirusTotal results
- **AIAnalysis** — Gemini AI generated summaries
- **PhishingDatabase** — Pre-seeded known phishing URLs

---

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Fatmah1211/PhishGuard.git
cd PhishGuard
```

### 2. Install Dependencies
```bash
pip install flask pyodbc requests google-genai python-dotenv --break-system-packages
```

### 3. Create .env File
DB_SERVER=your_windows_ip
DB_NAME=PhishGuardDB
DB_USER=phishguard_user
DB_PASSWORD=PhishGuard@123
VT_API_KEY=your_virustotal_key
GEMINI_API_KEY=your_gemini_key
### 4. Run the App
```bash
python3 app.py
```

---

## 👩‍💻 Team

| Member | Role |
|---|---|
| Fatima Tahir | Database & Backend Core |
| Ayesha Noor | Data Seeding & Integration Testing |
| Fizzah Ahsan | Frontend & Documentation |

---

## 🏫 Project Info

- **Course:** Database Systems
- **University:** University of Management and Technology, Lahore
- **Semester:** 4th Semester — BS Cybersecurity
