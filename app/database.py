from beanie import init_beanie
from app.connection import db
from app.db.models import EvidenceData

async def init_db():
    await init_beanie(database=db, document_models=[EvidenceData])
    counter_collection = await db.counter.find_one({"type": "user"})
    if counter_collection is None:
        await db.create_collection("counter")
        await db.counter.insert_one({"type": "user", "seq": 0})





