import os
from openai import OpenAI
from datetime import datetime

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
            response_text = completion.choices[0].message.content.strip()
            return response_text
        except Exception as e:
            return f"⚠️ Error: {str(e)}"

    def analyze_threat(self, query):
        prompt = f"""Analyze this cyber threat: {query}
Include details like attack vector, TTPs, IoCs, CVEs, and timeline.
Respond in clear, structured text."""
        return self._send_request(prompt)

    def tag_threat_data(self, data):
        prompt = f"""Tag the following cyber threat: {data}
Respond in clear, structured text with:
- attack_vector
- TTP
- threat_actor
- target_sector
- Severity Level"""
        return self._send_request(prompt)
