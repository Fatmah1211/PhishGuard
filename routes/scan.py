from flask import Blueprint, request, jsonify
import pyodbc
import requests
from google import genai
import json
import time
from config import CONNECTION_STRING, VT_API_KEY, GEMINI_API_KEY

scan_bp = Blueprint('scan', __name__)

client = genai.Client(api_key=GEMINI_API_KEY)

def get_db():
    return pyodbc.connect(CONNECTION_STRING)

def get_ai_summary(url, engines_flagged, total_engines, threat_category, stats):
    try:
        prompt = f"""
        A URL was scanned for phishing/malware. Here are the results:
        - URL: {url}
        - Engines flagged: {engines_flagged} out of {total_engines}
        - Threat category: {threat_category}
        - Stats: {stats}

        Give a 3-4 sentence plain English security assessment.
        State if it is safe or dangerous, why, and what the user should do.
        End with a risk level: Low, Medium, or High.
        """
        ai_response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return ai_response.text
    except Exception:
        return f"This URL was flagged by {engines_flagged} out of {total_engines} security engines as {threat_category}. {'Do not visit this URL.' if threat_category == 'malicious' else 'Exercise caution with this URL.' if threat_category == 'suspicious' else 'This URL appears safe.'}"

@scan_bp.route('/check', methods=['POST'])
def check_url():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT scan_id, status FROM ScanRequests WHERE url = ?", url)
    existing = cursor.fetchone()

    if existing:
        scan_id = existing[0]
        cursor.execute("SELECT summary, risk_level FROM AIAnalysis WHERE scan_id = ?", scan_id)
        ai_result = cursor.fetchone()
        conn.close()
        return jsonify({
            'url': url,
            'status': existing[1],
            'summary': ai_result[0] if ai_result else 'No summary available',
            'risk_level': ai_result[1] if ai_result else 'Unknown',
            'source': 'cache'
        })

    vt_url = "https://www.virustotal.com/api/v3/urls"
    headers = {"x-apikey": VT_API_KEY}
    response = requests.post(vt_url, headers=headers, data={"url": url})

    if response.status_code != 200:
        conn.close()
        return jsonify({'error': 'VirusTotal submission failed', 'details': response.text}), 500

    analysis_id = response.json()['data']['id']
    time.sleep(15)

    result_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    result = requests.get(result_url, headers=headers).json()

    stats = result['data']['attributes']['stats']
    engines_flagged = stats.get('malicious', 0) + stats.get('suspicious', 0)
    total_engines = sum(stats.values())
    threat_category = 'malicious' if stats.get('malicious', 0) > 0 else 'suspicious' if stats.get('suspicious', 0) > 0 else 'clean'

    if engines_flagged == 0:
        status = 'clean'
    elif engines_flagged <= 5:
        status = 'suspicious'
    else:
        status = 'malicious'

    cursor.execute("""
        INSERT INTO ScanRequests (url, status, vt_scan_id)
        OUTPUT INSERTED.scan_id
        VALUES (?, ?, ?)
    """, url, status, analysis_id)
    scan_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO ThreatReports (scan_id, engines_flagged, total_engines, threat_category, raw_result)
        VALUES (?, ?, ?, ?, ?)
    """, scan_id, engines_flagged, total_engines, threat_category, json.dumps(stats))

    summary = get_ai_summary(url, engines_flagged, total_engines, threat_category, stats)
    risk_level = 'High' if status == 'malicious' else 'Medium' if status == 'suspicious' else 'Low'

    cursor.execute("""
        INSERT INTO AIAnalysis (scan_id, summary, risk_level)
        VALUES (?, ?, ?)
    """, scan_id, summary, risk_level)

    conn.commit()
    conn.close()

    return jsonify({
        'url': url,
        'status': status,
        'engines_flagged': engines_flagged,
        'total_engines': total_engines,
        'summary': summary,
        'risk_level': risk_level,
        'source': 'live'
    })
