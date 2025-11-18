# main.py

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from pymongo import MongoClient
from pymongo.collection import Collection
from bson import ObjectId
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# --- Models (คงเดิม) ---
class Ritual(BaseModel):
    name: str
    description: str

class RitualResponse(Ritual):
    id: str = Field(..., alias="_id")

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True

# --- Lifespan Management ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application's lifespan.
    Connects to the database on startup and closes the connection on shutdown.
    """
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("MONGO_URI environment variable not found.")
    
    print("Connecting to the database...")
    app.state.mongo_client = MongoClient(mongo_uri)
    app.state.db = app.state.mongo_client["agio_memory"]
    print("Database connection successful.")
    
    yield # แอปพลิเคชันจะทำงาน ณ จุดนี้

    print("Closing database connection...")
    app.state.mongo_client.close()
    print("Database connection closed.")

# --- FastAPI App Initialization ---
app = FastAPI(lifespan=lifespan)

# --- Dependency for Database Collection ---
def get_rituals_collection() -> Collection:
    """Dependency to get the rituals collection from the app state."""
    return app.state.db["rituals"]

# --- Endpoints (ปรับแก้ให้ใช้ Depends) ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the Ritual Consecrator API"}

@app.post("/create_ritual/", response_model=RitualResponse)
def create_ritual(ritual: Ritual, db: Collection = Depends(get_rituals_collection)):
    ritual_dict = ritual.model_dump()
    inserted_id = db.insert_one(ritual_dict).inserted_id
    
    # ดึงข้อมูลที่เพิ่งสร้างเพื่อส่งกลับไป
    created_ritual = db.find_one({"_id": inserted_id})
    if created_ritual is None:
        raise HTTPException(status_code=500, detail="Failed to create and retrieve ritual.")
        
    return created_ritual

@app.get("/get_ritual/{ritual_id}", response_model=RitualResponse)
def get_ritual(ritual_id: str, db: Collection = Depends(get_rituals_collection)):
    try:
        obj_id = ObjectId(ritual_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ritual_id format.")

    ritual = db.find_one({"_id": obj_id})
    if ritual is None:
        raise HTTPException(status_code=404, detail="Ritual not found.")
    return ritual
