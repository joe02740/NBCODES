from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask import send_from_directory, redirect
from pymongo import MongoClient
import certifi
import os
from anthropic import Anthropic 
import anthropic
from openai import OpenAI
from dotenv import load_dotenv
from bson import json_util
import json


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
db = mongo_client['NBCODES']
collection = db['NBCODES']


@app.route('/')
def landing():
    return send_from_directory('.', 'index.html')

@app.route('/nbcodes')
def nbcodes():
    return redirect('/search')  # or wherever your main app starts

@app.route('/weights-measures')
def weights_measures():
    return "Weights and Measures App (Under Construction)"


@app.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get('q', '')
        search_type = request.args.get('type', 'atlas')  # Default to Atlas search

        if search_type == 'semantic':
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
                        "knnBeta": {
                            "vector": query_embedding,
                            "path": "embedding",
                            "k": 10
                        }
                    }
                },
                {
                    "$project": {
                        "NodeId": 1,
                        "Title": 1,
                        "Content": 1,
                        "Subtitle": 1,
                        "score": {"$meta": "searchScore"}
                    }
                }
            ]))
        else:
            # Atlas Search
            results = list(collection.aggregate([
                {
                    "$search": {
                        "index": "default",
                        "text": {
                            "query": query,
                            "path": ["Title", "Subtitle", "Content"]
                        }
                    }
                },
                {
                    "$project": {
                        "NodeId": 1,
                        "Title": 1,
                        "Subtitle": 1,
                        "Content": 1,
                        "score": {"$meta": "searchScore"}
                    }
                },
                {"$limit": 10}
            ]))

        # Convert ObjectId to string for JSON serialization
        for doc in results:
            doc['_id'] = str(doc['_id'])

        return jsonify(results)

    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({"error": str(e)}), 500




@app.route('/test_search', methods=['GET'])
def test_search():
    try:
        sample_docs = list(collection.find({}, {"NodeId": 1, "Title": 1, "Subtitle": 1, "Content": 1}).limit(5))
        
        # Convert ObjectId to string for JSON serialization
        for doc in sample_docs:
            doc['_id'] = str(doc['_id'])
        
        return jsonify({
            "sample_docs": sample_docs,
            "count": len(sample_docs)
        })
    except Exception as e:
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
        return render_template('table_of_contents.html', toc=toc)
    except Exception as e:
        print(f"Table of Contents error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/content/<node_id>')
def get_content(node_id):
    try:
        document = collection.find_one({"NodeId": node_id})
        if document:
            return render_template('content.html', document=document)
        else:
            return "Content not found", 404
    except Exception as e:
        print(f"Content retrieval error: {e}")
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