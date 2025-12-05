import asyncio
from app.core.supabase import supabase

async def seed_database():
    print("🌱 Seeding Database...")

    # 1. Create Subject
    subject_data = {"name": "Operating Systems", "description": "Core CS Subject for GATE"}
    res = supabase.table("subjects").insert(subject_data).execute()
    if not res.data:
        print("Subject already exists or failed.")
        # Try to fetch it if it exists
        res = supabase.table("subjects").select("*").eq("name", "Operating Systems").execute()
    
    subject_id = res.data[0]["id"]
    print(f"✅ Subject Created: {subject_id}")

    # 2. Create Units
    units = [
        {"name": "Process Management", "order_index": 1},
        {"name": "Deadlocks", "order_index": 2},
        {"name": "Memory Management", "order_index": 3}
    ]
    
    for unit in units:
        unit["subject_id"] = subject_id
        res = supabase.table("units").insert(unit).execute()
        unit_id = res.data[0]["id"]
        print(f"  ✅ Unit Created: {unit['name']}")

        # 3. Create Topics for Process Management
        if unit["name"] == "Process Management":
            topics = [
                {"name": "Process Lifecycle", "order_index": 1, "keywords": ["process state", "PCB", "context switch"]},
                {"name": "CPU Scheduling", "order_index": 2, "keywords": ["scheduling algorithms", "FCFS", "Round Robin"]},
                {"name": "Threads", "order_index": 3, "keywords": ["user threads", "kernel threads"]}
            ]
            for topic in topics:
                topic["unit_id"] = unit_id
                supabase.table("topics").insert(topic).execute()
                print(f"    ✅ Topic Created: {topic['name']}")

if __name__ == "__main__":
    asyncio.run(seed_database())
