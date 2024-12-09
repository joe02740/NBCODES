from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from google.generativeai import caching
import pandas as pd
import datetime
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

def load_city_codes():
    """Load and format city codes for context"""
    try:
        df = pd.read_csv('NewBedfordMACodeofOrdinancesEXPORT20240530.csv')
        # Format the codes into a structured text
        context_text = ""
        for _, row in df.iterrows():
            context_text += f"Chapter {row['Chapter']}, Section {row['Section']}: {row['Title']}\n"
            context_text += f"Content: {row['Content']}\n\n"
        return context_text
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

def initialize_context_cache():
    """Initialize Gemini context cache with city codes"""
    try:
        city_codes = load_city_codes()
        if not city_codes:
            raise Exception("Failed to load city codes")

        # Create a cache with a 24 hour TTL
        cache = caching.CachedContent.create(
            model='models/gemini-1.5-pro-001',
            display_name='nb_city_codes',
            system_instruction=(
                'You are an expert on New Bedford City Codes. Your role is to help '
                'users understand and navigate the city ordinances and regulations. '
                'Provide clear, accurate explanations in everyday language.'
            ),
            contents=[city_codes],
            ttl=datetime.timedelta(hours=24),
        )
        return cache
    except Exception as e:
        print(f"Error initializing context cache: {e}")
        return None

# Initialize the context cache when the app starts
context_cache = initialize_context_cache()
if context_cache:
    model = genai.GenerativeModel.from_cached_content(cached_content=context_cache)
else:
    model = genai.GenerativeModel("gemini-1.5-pro-001")

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"})

    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        response = model.generate_content(
            f"Based on the New Bedford City Codes provided in the context, please answer: {user_message}"
        )
        
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