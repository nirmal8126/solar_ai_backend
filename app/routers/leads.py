from fastapi import APIRouter
from app.schemas.lead_schema import LeadCreate
from app.database import supabase
from app.ai import calculate_system_size, generate_ai_summary
from app.utils import detect_utility_from_address
from app.pdf_generator import generate_proposal_pdf
import os

router = APIRouter(prefix="/leads", tags=["Leads"])

@router.get("/")
def get_all_leads():
    response = supabase.table("leads").select("*").execute()
    return response.data

@router.post("/")
def create_lead(lead: LeadCreate):
    system_size = calculate_system_size(
        avg_bill=lead.avg_monthly_bill,
        property_type=lead.property_type
    )

    utility = detect_utility_from_address(lead.address)

    data = {
        "customer_name": lead.customer_name,
        "email": lead.email,
        "phone": lead.phone,
        "address": lead.address,
        "property_type": lead.property_type,
        "avg_monthly_bill": lead.avg_monthly_bill,
        "status": "new",
    }

    result = supabase.table("leads").insert(data).execute()
    new_lead = result.data[0]

    ai_summary = generate_ai_summary(new_lead)

    # ensure proposals dir exists
    os.makedirs("proposals", exist_ok=True)
    file_path = f"proposals/proposal_{new_lead['id']}.pdf"
    generate_proposal_pdf(new_lead, ai_summary, file_path)

    supabase.table("leads").update({
        "ai_summary": ai_summary,
        "proposal_path": file_path,
    }).eq("id", new_lead["id"]).execute()

    return {
        "message": "Lead created with AI proposal",
        "lead": {**new_lead, "system_size_kw": system_size},
        "ai_summary": ai_summary,
    }

@router.get("/{lead_id}")
def get_lead(lead_id: int):
    result = supabase.table("leads").select("*").eq("id", lead_id).single().execute()
    return result.data

@router.put("/{lead_id}")
def update_status(lead_id: int, data: dict):
    response = supabase.table("leads").update(data).eq("id", lead_id).execute()
    return {"message": "Status updated", "lead": response.data}

@router.get("/{lead_id}/proposal")
def get_proposal(lead_id: int):
    result = supabase.table("leads").select("proposal_path").eq("id", lead_id).single().execute()
    path = result.data.get("proposal_path")

    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Proposal not generated")

    return FileResponse(path, media_type="application/pdf", filename=os.path.basename(path))


@router.post("/{lead_id}/roof-analyze")
def analyze_roof(lead_id: int):
    """
    Placeholder: in future this will call a GIS / satellite API.
    For now we just return a dummy suggestion.
    """
    result = supabase.table("leads").select("*").eq("id", lead_id).single().execute()
    lead = result.data

    # Dummy logic: assume 100 sqft per kW
    if lead and lead.get("system_size_kw"):
        roof_area = float(lead["system_size_kw"]) * 100
        max_size = lead["system_size_kw"]
    else:
        roof_area = 300.0
        max_size = 3.0

    supabase.table("leads").update({
        "roof_area_sqft": roof_area,
        "max_system_size_kw": max_size,
        "roof_notes": "Placeholder estimate. Connect real roof AI later."
    }).eq("id", lead_id).execute()

    return {
        "roof_area_sqft": roof_area,
        "max_system_size_kw": max_size,
        "roof_notes": "Placeholder estimate. Connect real roof AI later.",
    }


