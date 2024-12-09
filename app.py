from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from datetime import timedelta
import pandas as pd

app = Flask(__name__)
CORS(app)

# Initialize Gemini
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Load the CSV file once when the app starts
def load_city_codes():
    df = pd.read_csv('NewBedfordMACodeofOrdinancesEXPORT20240530.csv')
    return df.to_string()  # Convert entire DataFrame to string for context

city_codes = load_city_codes()

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        # Create cache with the city codes
        cache = genai.caching.CachedContent.create(
            model='models/gemini-1.5-pro-001',
            display_name='nb_city_codes',
            system_instruction=(
                'You are an expert on New Bedford city codes. Provide accurate, helpful answers '
                'based on the official city codes. If a specific code section is relevant, '
                'cite it in your response.'
            ),
            contents=[city_codes],
            ttl=timedelta(hours=1)
        )
        
        # Initialize model with cache
        model = genai.GenerativeModel.from_cached_content(cached_content=cache)
        
        # Generate response
        response = model.generate_content(user_message)
        
        return jsonify({
            "response": response.text,
            "usage": response.usage_metadata
        })
        
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)