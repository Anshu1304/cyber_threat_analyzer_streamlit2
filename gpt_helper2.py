import os
import json
from openai import OpenAI

class GPTHelper:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "missing_key")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            default_headers={
                "HTTP-Referer": "https://streamlit.io/",
                "X-Title": "Cyber Threat Analyzer"
            }
        )
        self.model = "google/gemma-3-12b-it:free"

    def _send_request(self, prompt):
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1024
            )
            text = completion.choices[0].message.content.strip()
            try:
                return {"status": "success", "format": "json", "data": json.loads(text)}
            except:
                return {"status": "success", "format": "text", "data": {"content": text}}
        except Exception as e:
            return {"error": str(e)}

    def analyze_threat(self, query):
        prompt = f"""You are a cybersecurity expert analyzing threat data.
Provide detailed, factual responses about cyber threats, attack vectors, and TTPs.
Format your response as JSON with the following structure:
{{
    "Attack_Vector": "How the attack was carried out (e.g., Phishing, Ransomware, SQL Injection)",
    "TTPs": {{
        "Tactics": "High-level objectives of the attacker (e.g., Initial Access, Persistence, Exfiltration)",
        "Techniques": "Specific methods used (e.g., Spear Phishing, Credential Dumping)",
        "Procedures": "Detailed execution steps"
    }},
    "Indicators_of_Compromise": {{
        "IP_Addresses": ["List of malicious IPs (if available)"],
        "File_Hashes": ["List of malware file hashes"],
        "Domains": ["Malicious domains used in the attack"]
    }},
    "CVE_Associated": "If the attack exploits a known vulnerability, mention its CVE number",
    "Attack_Timeline": {{
        "Reconnaissance": "Did the attack involve pre-attack scanning?",
        "Initial_Compromise": "How did the attacker gain access?",
        "Lateral_Movement": "Did the attacker move across the network?",
        "Data_Exfiltration": "Was sensitive data stolen?",
        "Persistence": "Did the attacker establish long-term access?"
    }},
    "Incident_Reports": ["Reference any similar past attacks (e.g., FireEye, CrowdStrike reports)"],
    "Threat_Intelligence_Feed": ["Any updates from cybersecurity feeds (e.g., AlienVault, Recorded Future)?"]
}}

Query: {query}

Please provide your analysis in the specified JSON format."""
        return self._send_request(prompt)

    def tag_threat_data(self, data):
        prompt = f"""Tag the following cyber threat data with relevant categories.
Respond in JSON format:
{{
    "TTPs": {{
        "Tactics": ["List of high-level objectives"],
        "Techniques": ["List of specific methods used"],
        "Procedures": ["Detailed execution steps"]
    }},
    "Attack_Vector": ["Primary attack methods (e.g., Phishing, Ransomware)"],
    "Indicators_of_Compromise": {{
        "IP_Addresses": ["List of known malicious IPs"],
        "File_Hashes": ["List of associated malware hashes"],
        "Domains": ["Suspicious domains used"]
    }},
    "Affected_Industries": ["Which industries were targeted (e.g., Finance, Healthcare)"],
    "Severity_Level": ["One of: Low, Medium, High, Critical"]
}}
Data: {data}"""
        return self._send_request(prompt)
