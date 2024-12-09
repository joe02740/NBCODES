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

# Initialize Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro-001")

def load_city_codes():
    """Load city codes from JSON file with proper encoding"""
    try:
        # Using the same encoding that worked for CSV conversion
        with open('city_codes.json', 'r', encoding='cp1252') as file:
            codes = json.load(file)
            print(f"Successfully loaded {len(codes)} city code entries")
            return codes
    except UnicodeDecodeError:
        print("Encoding error, trying UTF-8...")
        try:
            with open('city_codes.json', 'r', encoding='utf-8') as file:
                codes = json.load(file)
                print(f"Successfully loaded {len(codes)} city code entries")
                return codes
        except Exception as e:
            print(f"Error loading with UTF-8: {e}")
            return []
    except Exception as e:
        print(f"Error loading city codes: {e}")
        return []

# Load city codes at startup
print("Loading city codes...")
city_codes = load_city_codes()
if not city_codes:
    print("Warning: No city codes were loaded!")

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"})

    try:
        if not city_codes:
            return jsonify({
                "error": "City codes database is not available",
                "status": "error"
            }), 500

        data = request.get_json()
        user_message = data.get('message', '')
        
        # Simple keyword matching to find relevant sections
        keywords = user_message.lower().split()
        relevant_codes = []
        
        for code in city_codes:
            content = str(code.get('Content', '')).lower()
            title = str(code.get('Title', '')).lower()
            if any(keyword in content or keyword in title for keyword in keywords):
                relevant_codes.append(code)
        
        # Limit to 3 most relevant sections
        relevant_codes = relevant_codes[:3]
        
        # Build context from relevant codes
        context = "\n".join([
            f"Chapter {code.get('Chapter', '')}, Section {code.get('Section', '')}: "
            f"{code.get('Title', '')}\n{code.get('Content', '')}"
            for code in relevant_codes
        ])

        prompt = (
            f"Context from New Bedford City Codes:\n{context}\n\n"
            f"User Question: {user_message}\n\n"
            "Please explain the relevant city codes in clear, everyday language. "
            "If the context doesn't directly answer the question, say so."
        )

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