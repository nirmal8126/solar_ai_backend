from fastapi import APIRouter
from app.ai import generate_ai_summary

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/")
def chat_ai(data: dict):
    user_msg = data["message"]
    ai_reply = generate_ai_summary({
        "customer_name": "Customer",
        "city": "Unknown",
        "avg_monthly_bill": 2000
    })
    return {"reply": ai_reply}
