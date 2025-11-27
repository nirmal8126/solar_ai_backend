from datetime import datetime
from typing import Optional
import uuid

class Lead:
    """Lead model for storing customer information"""
    
    def __init__(
        self,
        name: str,
        email: str,
        phone: str,
        location: str,
        interest_type: str,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        status: str = "new"
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.phone = phone
        self.location = location
        self.interest_type = interest_type
        self.status = status
        self.created_at = created_at or datetime.utcnow()
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
            "interest_type": self.interest_type,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
