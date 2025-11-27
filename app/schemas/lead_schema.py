from pydantic import BaseModel

class LeadCreate(BaseModel):
    customer_name: str
    email: str
    phone: str
    address: str
    property_type: str
    avg_monthly_bill: float

class Lead(LeadCreate):
    id: int
