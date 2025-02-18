# In core/analysis.py
from openai import OpenAI

class LLMAnalyzer:
    def analyze_esg(self, text):
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Analyze ESG risks:\n{text}"}]
        )
        return response.choices[0].message.content