from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://nbcodes.netlify.app",
            "http://localhost:3000"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize Gemini with specific parameters
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
generation_config = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
}
model = genai.GenerativeModel("gemini-1.5-pro-001", generation_config=generation_config)

def load_city_codes():
    try:
        with open('city_codes.json', 'r', encoding='cp1252') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading city codes: {e}")
        return []

city_codes = load_city_codes()

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"})

    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        
        # Find relevant code sections
        relevant_codes = []
        keywords = user_message.split()
        
        for code in city_codes:
            content = str(code.get('Content', '')).lower()
            title = str(code.get('Title', '')).lower()
            if any(keyword in content or keyword in title for keyword in keywords):
                relevant_codes.append(code)
        
        relevant_codes = relevant_codes[:3]  # Limit to top 3 matches
        
        if not relevant_codes:
            # No relevant codes found
            response = model.generate_content(
                f"I've searched the New Bedford City Codes but couldn't find any sections directly related to '{user_message}'. "
                "Would you like to rephrase your question or ask about something else?"
            )
            return jsonify({"response": response.text, "status": "success"})

        # Format context more explicitly
        formatted_context = "Here are the relevant sections of the New Bedford City Codes:\n\n"
        for code in relevant_codes:
            formatted_context += f"""SECTION REFERENCE:
Chapter: {code.get('Chapter', 'N/A')}
Section: {code.get('Section', 'N/A')}
Title: {code.get('Title', 'N/A')}
Content: {code.get('Content', 'N/A')}
-------------------\n"""

        prompt = f"""You are an expert on New Bedford City Codes helping a resident understand local regulations.
Below are relevant sections from the official city codes. Please explain them in simple, everyday language.

{formatted_context}

User's Question: {user_message}

Please provide:
1. A clear explanation of what these codes mean in everyday language
2. The main purpose of these regulations
3. How they might apply to the user's situation

If any part is unclear or if the codes don't fully address the question, please say so."""

        response = model.generate_content(prompt)
        
        return jsonify({
            "response": response.text,
            "status": "success"
        })

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)