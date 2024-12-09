import os
from pymongo import MongoClient
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

# MongoDB connection
connection_string = os.getenv('MONGODB_URI')
mongo_client = MongoClient(connection_string)
db = mongo_client.NBCODES
collection = db.NBCODES

# OpenAI client setup
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def create_embedding(text):
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def update_embeddings():
    total_docs = collection.count_documents({})
    for doc in tqdm(collection.find({}), total=total_docs):
        text = f"{doc.get('Title', '')} {doc.get('Subtitle', '')} {doc.get('Content', '')}"
        embedding = create_embedding(text)
        
        collection.update_one(
            {'_id': doc['_id']},
            {'$set': {'embedding': embedding}}
        )

    print("All documents processed and embeddings created")

if __name__ == "__main__":
    update_embeddings()