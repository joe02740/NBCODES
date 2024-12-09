import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def inspect_mongodb():
    # Get the connection string from the environment variable
    connection_string = os.getenv('MONGODB_URI')
    
    if not connection_string:
        print("Error: MONGODB_URI environment variable not set.")
        return

    print(f"Attempting to connect with URI: {connection_string}")

    try:
        # Connect to MongoDB
        client = MongoClient(connection_string)
        print("Successfully connected to MongoDB")

        # List all databases
        databases = client.list_database_names()
        print("\nAvailable databases:")
        for db_name in databases:
            print(f"- {db_name}")
            db = client[db_name]
            
            # List collections in each database
            collections = db.list_collection_names()
            print(f"  Collections in {db_name}:")
            for collection_name in collections:
                print(f"  - {collection_name}")
                
                # Count documents in each collection
                count = db[collection_name].count_documents({})
                print(f"    Document count: {count}")

                # Sample document (if any)
                sample = db[collection_name].find_one()
                if sample:
                    print("    Sample document fields:")
                    for key in sample.keys():
                        print(f"      - {key}")

                # Check for 'embedding' field
                embedding_count = db[collection_name].count_documents({"embedding": {"$exists": True}})
                print(f"    Documents with 'embedding' field: {embedding_count}")

                print()  # Empty line for readability

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if 'client' in locals():
            client.close()
            print("\nMongoDB connection closed")

if __name__ == "__main__":
    inspect_mongodb()