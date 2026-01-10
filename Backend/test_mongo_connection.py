from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")

client = MongoClient(uri)

try:
    client.admin.command("ping")
    print("✅ MongoDB authentication successful!")

    db = client[db_name]
    print(f"📦 Database: {db_name}")
    print("📂 Collections:", db.list_collection_names())

except Exception as e:
    print("❌ Authentication failed")
    print(e)
