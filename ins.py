import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv('MONGODB_URI')
client = MongoClient(connection_string)

def check_database(db_name):
    db = client[db_name]
    collection = db.NBCODES
    
    print(f"\nChecking database: {db_name}")
    
    # Check for embeddings
    docs_with_embedding = collection.count_documents({"embedding": {"$exists": True}})
    print(f"Documents with 'embedding' field: {docs_with_embedding}")
    
    # Check indexes
    print("Indexes:")
    for index in collection.list_indexes():
        print(f"- {index['name']}: {index['key']}")
    
    # Sample document
    sample_doc = collection.find_one({}, {"_id": 0, "NodeId": 1, "Title": 1, "embedding": 1})
    if sample_doc:
        print("\nSample document:")
        for key, value in sample_doc.items():
            if key == "embedding":
                print(f"{key}: {type(value)} with length {len(value) if isinstance(value, list) else 'N/A'}")
            else:
                print(f"{key}: {value}")

# Check both databases
check_database('NBCODES')
check_database('joseph1914')

client.close()