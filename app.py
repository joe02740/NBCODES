from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import certifi
import os
from anthropic import Anthropic 
import anthropic
from dotenv import load_dotenv

load_dotenv()



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://nbcodes-qeq1rll2l-josephs-projects-45363c9f.vercel.app", "https://nbcodes.vercel.app"]}})


# Initialize the Anthropic client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

#MONGODB Connection string
connection_string = os.getenv('MONGODB_URI')


# MongoDB connection
connection_string = os.getenv('MONGODB_URI')
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

    try:
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": f"Explain the following New Bedford city code in simple terms: {context}\n\nUser query: {query}"}
            ]
        )
        explanation = message.content[0].text
        return jsonify({"explanation": explanation})
    except Exception as e:
        print(f"Error in ai_explain: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    try:
        result = list(collection.find().limit(1))
        return jsonify(result)
    except Exception as e:
        print(f"Test error: {e}")
        return jsonify({"error": str(e)}), 500
    



@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == "OPTIONS":
        return {"message": "OK"}, 200
    
    print("Chat endpoint accessed")
    
    data = request.json
    user_message = data.get('message')
    context = data.get('context')

    print(f"Received message: {user_message}")
    print(f"Context: {context}")

    try:
        print("Attempting to create message with Anthropic API")
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": f"Context: {context}\n\nHuman: {user_message}"}
            ]
        )
        print("Successfully created message with Anthropic API")
        
        ai_response = message.content[0].text
        print(f"AI Response: {ai_response[:100]}...")
        
        return jsonify({"response": ai_response})
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)