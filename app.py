from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import certifi
import os
from anthropic import Anthropic 
import anthropic
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://nbcodes.netlify.app", "https://nbcodes.com", "https://www.nbcodes.com"]}})

# Initialize the Anthropic client
anthropic_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Initialize the OpenAI client
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# MongoDB connection
connection_string = os.getenv('MONGODB_URI')
mongo_client = MongoClient(connection_string, tlsCAFile=certifi.where())
db = mongo_client.NBCODES
collection = db.NBCODES

@app.route('/', methods=['GET'])
def home():
    return "Hello, World!"

@app.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get('q', '')
        print(f"Received search query: {query}")
        
        # Create embedding for the query
        response = openai_client.embeddings.create(
            input=query,
            model="text-embedding-ada-002"
        )
        query_embedding = response.data[0].embedding

        # Perform semantic search using the embedding
        results = list(collection.aggregate([
            {
                "$search": {
                    "index": "vector_index1",  # Make sure this matches your index name
                    "knnBeta": {
                        "vector": query_embedding,
                        "path": "embedding",
                        "k": 10
                    }
                }
            },
            {
                "$project": {
                    "NodeId": 1, "Title": 1, "Content": 1, "Subtitle": 1,
                    "score": {"$meta": "searchScore"}
                }
            }
        ]))
        
        print(f"Found {len(results)} results with vector search")

        if not results:
            # Fallback to simple text search if vector search returns no results
            results = list(collection.find(
                {"$text": {"$search": query}},
                {"NodeId": 1, "Title": 1, "Content": 1, "Subtitle": 1, "score": {"$meta": "textScore"}}
            ).sort([("score", {"$meta": "textScore"})]).limit(10))
            print(f"Found {len(results)} results with text search")

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
        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=444,
            messages=[
                {"role": "user", "content": f"Please simplify the New Bedford MA city code and put it in every day language where possible: {context}\n\nUser query: {query}"}
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

@app.route('/table_of_contents', methods=['GET'])
def get_table_of_contents():
    try:
        pipeline = [
            {"$sort": {"Chapter": 1, "Section": 1, "Subsection": 1}},
            {"$group": {
                "_id": {
                    "Chapter": "$Chapter",
                    "Section": "$Section",
                    "Subsection": "$Subsection"
                },
                "items": {
                    "$push": {
                        "NodeId": "$NodeId",
                        "Title": "$Title",
                        "Subtitle": "$Subtitle"
                    }
                }
            }},
            {"$group": {
                "_id": {"Chapter": "$_id.Chapter", "Section": "$_id.Section"},
                "subsections": {
                    "$push": {
                        "Subsection": "$_id.Subsection",
                        "items": "$items"
                    }
                }
            }},
            {"$group": {
                "_id": "$_id.Chapter",
                "sections": {
                    "$push": {
                        "Section": "$_id.Section",
                        "subsections": "$subsections"
                    }
                }
            }},
            {"$sort": {"_id": 1}}
        ]
        
        toc = list(collection.aggregate(pipeline))
        return jsonify(toc)
    except Exception as e:
        print(f"Table of Contents error: {e}")
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
        message = anthropic_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=777,
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