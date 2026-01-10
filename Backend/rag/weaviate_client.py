import weaviate
import os
from dotenv import load_dotenv
from weaviate.classes.init import Auth

load_dotenv()

# ✅ v4 SYNTAX - connect_to_weaviate_cloud
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=os.getenv("WEAVIATE_URL"),
    auth_credentials=Auth.api_key(os.getenv("WEAVIATE_API_KEY"))
)

print("✅ Weaviate v4 client connected successfully")
