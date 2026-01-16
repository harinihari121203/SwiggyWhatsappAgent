from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from agent.offer_agent import OfferAgent
from agent.customer_support_agent import CustomerSupportAgent
from agent.intent_router import detect_intent


# -------------------------
# Lifespan
# -------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    support_agent.close()


# -------------------------
# Create FastAPI app FIRST
# -------------------------
app = FastAPI(lifespan=lifespan)


# -------------------------
# CORS Middleware (AFTER app creation)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all for now
    allow_credentials=True,
    allow_methods=["*"],   # allows OPTIONS
    allow_headers=["*"],
)


# -------------------------
# Agents
# -------------------------
offer_agent = OfferAgent()
support_agent = CustomerSupportAgent()


# -------------------------
# Models
# -------------------------
class ChatRequest(BaseModel):
    message: str


# -------------------------
# Routes
# -------------------------
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
