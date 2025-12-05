from fastapi import APIRouter, HTTPException
from app.core.supabase import supabase
from app.models.syllabus import Subject, Unit, Topic

router = APIRouter()

@router.get("/subjects", response_model=list[Subject])
async def get_subjects():
    """Fetch all available subjects."""
    response = supabase.table("subjects").select("*").execute()
    return response.data

@router.get("/subjects/{subject_id}/syllabus", response_model=Subject)
async def get_syllabus(subject_id: str):
    """Fetch the full syllabus (Units -> Topics) for a subject."""
    
    # 1. Fetch Subject
    subj_response = supabase.table("subjects").select("*").eq("id", subject_id).execute()
    if not subj_response.data:
        raise HTTPException(status_code=404, detail="Subject not found")
    subject_data = subj_response.data[0]

    # 2. Fetch Units
    units_response = supabase.table("units").select("*").eq("subject_id", subject_id).order("order_index").execute()
    units_data = units_response.data

    # 3. Fetch Topics for all these units
    # We collect all unit IDs to do a single query
    unit_ids = [u["id"] for u in units_data]
    if unit_ids:
        topics_response = supabase.table("topics").select("*").in_("unit_id", unit_ids).order("order_index").execute()
        all_topics = topics_response.data
    else:
        all_topics = []

    # 4. Nest Topics into Units
    # Create a map for easier lookup
    units_map = {u["id"]: {**u, "topics": []} for u in units_data}
    
    for topic in all_topics:
        if topic["unit_id"] in units_map:
            units_map[topic["unit_id"]]["topics"].append(topic)

    # 5. Assemble final response
    subject_data["units"] = list(units_map.values())
    
    return subject_data
