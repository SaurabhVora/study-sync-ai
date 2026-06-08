import os
import google.generativeai as genai
from typing import List
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class GeminiSyllabusService:
    def __init__(self):
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            print("Warning: GEMINI_API_KEY not found. Syllabus generation will be disabled.")
            self.model = None

    def generate_syllabus(self, topic: str) -> List[str]:
        if not self.model:
            return []

        print(f"Asking Gemini for syllabus on: {topic}")
        
        prompt = (
            f"I am building a study playlist for the topic: '{topic}'. "
            f"Please list 5 to 7 core specific sub-topics or prerequisites that one must learn "
            f"to understand '{topic}' thoroughly. "
            f"Return ONLY the sub-topics as a comma-separated list. No numbering, no extra text."
        )

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            # Clean up and split
            topics = [t.strip() for t in text.split(',') if t.strip()]
            return topics
        except Exception as e:
            print(f"Error: Gemini Error: {e}")
            return []

gemini_service = GeminiSyllabusService()
