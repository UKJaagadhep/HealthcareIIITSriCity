import requests
import json

class MedicalTranscriptProcessor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama3-8b-8192"

    def extract_medical_info(self, transcript):
        if not transcript:
            return {'error': 'No transcript provided'}
        
        prompt = f"""
        Extract key medical information from the following transcript and return it in a very structured format without any regex.
        Don't include any information that is not given in the transcript.
        Medical Transcript:
        {transcript}
        """
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        try:
            response = requests.post(self.endpoint, headers=headers, json=payload)
            if response.status_code == 200:
                response_json = response.json()
                extracted_content = response_json.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                return extracted_content
            else:
                return {"error": f"API request failed with status code {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
