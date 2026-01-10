
from agent.customer_support_agent import CustomerSupportAgent
import os
from dotenv import load_dotenv

load_dotenv()

def test_agent():
    print("Testing CustomerSupportAgent with Groq...")
    try:
        agent = CustomerSupportAgent()
        print("✅ CustomerSupportAgent initialized successfully.")
        
        # We can't easily test a query without Weaviate being up and populated, 
        # but initialization confirms imports and API key presence (mostly).
        
        print("Agent configuration:")
        print(f" LLM Model: {agent.llm.model_name}")
        print(f" Embeddings Model: {agent.embeddings.model_name}")
        
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
    finally:
        if 'agent' in locals():
            agent.close()
            print("✅ Agent connection closed.")

if __name__ == "__main__":
    test_agent()
