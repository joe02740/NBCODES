from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
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

# Load the entire city code text at startup
print("Loading city codes...")
try:
    with open('city_codes.txt', 'r', encoding='utf-8') as f:
        CITY_CODES = f.read()
    print("City codes loaded successfully!")
except Exception as e:
    print(f"Error loading city codes: {e}")
    CITY_CODES = None

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"})

    if not CITY_CODES:
        return jsonify({
            "error": "City codes not available",
            "status": "error"
        }), 500

    try:
        data = request.get_json()
        user_message = data.get('message', '')

        prompt = f"""You are a helpful AI assistant with direct access to the New Bedford City Codes. 
Here are the complete city codes for reference:

{CITY_CODES}

Based on these official city codes, please answer the following question:
{user_message}

Remember: You have the complete New Bedford City Codes available to you in the text above. 
Please provide a clear, everyday-language explanation based on these specific codes."""

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