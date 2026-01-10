import os
import weaviate
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings  # ✅ FREE
from weaviate.classes.init import Auth
from weaviate.classes.config import Property, DataType

load_dotenv()
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY)
)
print("✅ Weaviate Connected")

def embed_offer_pdf(pdf_path="OfferData/swiggy_customer_offers_rag_training.pdf"):
    if not os.path.exists(pdf_path):
        print("❌ Create OfferData/ folder and add your PDF first")
        return

    print(f"📄 Loading {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    print(f"✂️ Split into {len(chunks)} chunks")

    # ✅ FREE LOCAL EMBEDDINGS - NO QUOTA LIMITS
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    collection_name = "OfferDocs"
    
    try:
        collection = client.collections.get(collection_name)
        print("✅ Using existing collection")
    except:
        print("📦 Creating collection")
        collection = client.collections.create(
            name=collection_name,
            properties=[
                Property(name="text", data_type=DataType.TEXT),
                Property(name="source", data_type=DataType.TEXT)
            ]
        )
    
    print("🚀 Embedding with FREE local model...")
    with collection.batch.dynamic() as batch:
        for i, chunk in enumerate(chunks):
            vector = embeddings.embed_query(chunk.page_content)
            batch.add_object(
                properties={"text": chunk.page_content, "source": pdf_path},
                vector=vector
            )
            if (i + 1) % 10 == 0:
                print(f"   {i+1}/{len(chunks)}")
    
    client.close()
    print(f"🎉 SUCCESS: {len(chunks)} chunks embedded!")

if __name__ == "__main__":
    embed_offer_pdf()
