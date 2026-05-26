import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ASI1_API_KEY")

BASE_URL = "https://api.asi1.ai/v1/chat/completions"


class AIService:

    @staticmethod
    def ask_ai(message: str):

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "asi1",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are NovaMind AI "
                        "for a Student Management System."
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            "temperature": 0.3
        }

        response = requests.post(
            BASE_URL,
            headers=headers,
            json=payload
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]
    
    @staticmethod
    def generate_student_insights(student):

        import json

        marks_data = {
            m.subject.name: m.marks
            for m in student.marks
        }

        prompt = f"""
        You are an academic performance analyst.

        Use ONLY the provided student data.
        Do NOT invent marks, subjects, grades,
        or recommendations outside the data.

        Return ONLY valid JSON.

        Student Name:
        {student.name}

        Subject Marks:
        {json.dumps(marks_data)}

        Generate:
        1. performance summary
        2. strengths
        3. weaknesses
        4. improvement suggestions

        Format:

        {{
          "summary": "...",
          "strengths": [],
          "weaknesses": [],
          "suggestions": []
        }}
        """

        result = AIService.ask_ai(prompt)
        result = result.strip()

        if result.startswith("```json"):
            result = result.replace("```json", "")

        if result.endswith("```"):
            result = result[:-3]

        result = result.strip()

        try:
            return json.loads(result)

        except json.JSONDecodeError:
            return {
                "error": (
                    "AI returned invalid JSON format"
                ),
                "raw_response": result
            }
    

    @staticmethod
    def generate_class_report(students):

        import json

        student_data = []

        for s in students:

            student_data.append({
                "name": s.name,
                "percentage": s.percentage,
                "grade": s.grade
            })

        prompt = f"""
        You are an educational analytics AI.

        Use ONLY provided data.
        Do NOT invent marks, subjects, grades,
        or recommendations outside the data.

        Return ONLY valid JSON.

        Student Data:
        {json.dumps(student_data)}

        Generate:
        1. class performance summary
        2. trends
        3. recommendations

        Format:

        {{
          "summary": "...",
          "trends": [],
          "recommendations": []
        }}
        """

        result = AIService.ask_ai(prompt)
        result = result.strip()

        if result.startswith("```json"):
            result = result.replace("```json", "")

        if result.endswith("```"):
            result = result[:-3]

        result = result.strip()

        try:
            return json.loads(result)

        except json.JSONDecodeError:
            return {
                "error": (
                    "AI returned invalid JSON format"
                ),
                "raw_response": result
            }
    
    