from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import certifi
import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# MongoDB connection
connection_string = 'mongodb+srv://joseph1914:NewBed777%24%24%24@cluster0.9tp0idi.mongodb.net/joseph1914?retryWrites=true&w=majority'
mongo_client = MongoClient(connection_string, tlsCAFile=certifi.where())
db = mongo_client.joseph1914
collection = db.NBCODES

@app.route('/', methods=['GET'])
def home():
    return "Hello, World!"


@app.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get('q', '')
        results = list(collection.find(
            {"$text": {"$search": query}},
            {"NodeId": 1, "Title": 1, "Content": 1, "Subtitle": 1, "_id": 0}
        ).limit(10))
        return jsonify(results)
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/ai_explain', methods=['POST'])
def ai_explain():
    data = request.json
    query = data.get('query')
    context = data.get('context')

    prompt = f"Human: Explain the following New Bedford city code in simple terms: {context}\n\nUser query: {query}\n\nAssistant:"

    try:
        response = client.completions.create(
            model="claude-2.1",
            prompt=prompt,
            max_tokens_to_sample=300
        )
        explanation = response.completion
        return jsonify({"explanation": explanation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    try:
        result = list(collection.find().limit(1))
        return jsonify(result)
    except Exception as e:
        print(f"Test error: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get('q', '')
        results = list(collection.find(
            {"$text": {"$search": query}},
            {"NodeId": 1, "Title": 1, "Content": 1, "Subtitle": 1, "_id": 0}
        ).limit(10))
        
        if not results:
            return jsonify({"message": "No results found for your search query."}), 404
        
        return jsonify(results)
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({"error": str(e)}), 500


    
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    context = data.get('context')

    # Construct the prompt for the AI
    prompt = f"Human: Context: {context}\n\nHuman: {user_message}\n\nAssistant:"

    try:
        response = client.completions.create(
            model="claude-2.1",
            prompt=prompt,
            max_tokens_to_sample=300
        )
        ai_response = response.completion

        return jsonify({"response": ai_response})
    except Exception as e:
        print(f"Error in chat: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)