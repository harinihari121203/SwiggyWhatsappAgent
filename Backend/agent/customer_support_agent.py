from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from rag.weaviate_client import client

class CustomerSupportAgent:

    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.2
        )
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
    
    def close(self):
        """Close the Weaviate client connection."""
        try:
            if client.is_connected():
                client.close()
        except:
            pass

    def answer(self, query: str) -> str:
        query_vector = self.embeddings.embed_query(query)

        collection = client.collections.get("OfferDocs")
        
        result = collection.query.near_vector(
            near_vector=query_vector,
            limit=3,
            return_properties=["text"]
        )

        context = "\n".join(
            item.properties["text"]
            for item in result.objects
        )

        prompt = f"""
        You are a Swiggy customer support assistant.
        Answer ONLY using the context below.
        If the user asks if they are eligible for offer ask them to enter their 10 digit phone number to verify with their order history.
        Context:
        {context}

        Question:
        {query}
        """

        response = self.llm.invoke(prompt)
        return response.content
