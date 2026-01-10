from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from agent.offer_agent import OfferAgent
from agent.customer_support_agent import CustomerSupportAgent
from agent.intent_router import detect_intent

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic (if any)
    yield
    # Shutdown logic
    support_agent.close()

app = FastAPI(lifespan=lifespan)

offer_agent = OfferAgent()
support_agent = CustomerSupportAgent()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    intent = detect_intent(req.message)

    if intent == "MOBILE_NUMBER":
        return offer_agent.check_offer_eligibility(req.message)

    return {
        "response": support_agent.answer(req.message)
    }

@app.post("/check-offer")
def check_offer(req: ChatRequest):
    return offer_agent.check_offer_eligibility(req.message)
