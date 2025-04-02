import os
import base64
from dotenv import load_dotenv
from bson import ObjectId
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
import motor.motor_asyncio


app = FastAPI()
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

def object_id_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, list):
        return [object_id_to_str(item) for item in obj]
    if isinstance(obj, dict):
        return {key: object_id_to_str(value) for key, value in obj.items()}
    return obj
def decode_base64_content(doc):
    if "content" in doc:
        doc["content"] = base64.b64decode(doc["content"])
    return doc

# Connect to Mongo Atlas
# Database connection as a dependency
async def get_database():
    # Create a new client for each request
    client = motor.motor_asyncio.AsyncIOMotorClient(
        mongo_uri,
        maxPoolSize=1,
        minPoolSize=0,
        serverSelectionTimeoutMS=5000
    )
    try:
        yield client.multimedia_db
    finally:
        client.close()  # Ensure connection is closed after request

class PlayerScore(BaseModel):
    player_name: str
    score: int

@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.post("/upload_sprite")
async def upload_sprite(file: UploadFile = File(...), db=Depends(get_database)):
    content = await file.read()
    encoded_content = base64.b64encode(content).decode('utf-8')
    sprite_doc = {"filename": file.filename, "content": encoded_content}
    result = await db.sprites.insert_one(sprite_doc)
    return {"message": "Sprite uploaded", "id": str(result.inserted_id)}

@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...), db=Depends(get_database)):
    content = await file.read()
    encoded_content = base64.b64encode(content).decode('utf-8')
    audio_doc = {"filename": file.filename, "content": encoded_content}
    result = await db.audio.insert_one(audio_doc)
    return {"message": "Audio file uploaded", "id": str(result.inserted_id)}

@app.post("/player_score")
async def add_score(score: PlayerScore,db=Depends(get_database)):
    score_doc = score.dict()
    result = await db.scores.insert_one(score_doc)
    return {"message": "Score recorded", "id": str(result.inserted_id)}

@app.get("/get_sprite")
async def get_sprites(sprite_name:str,db=Depends(get_database)):
    sprites = await db.sprites.find_one({"filename": sprite_name})
    return {"filename": sprites["filename"], "content": sprites["content"]}

@app.get("/get_audio_files")
async def get_audio_files(audio_name:str,db=Depends(get_database)):
    audio_files = await db.audio.find_one({"filename": audio_name})
    return {"filename": audio_files["filename"], "content": audio_files["content"]}

@app.get("/get_player_scores")
async def get_player_scores(player_name:str,db=Depends(get_database)):
    player_scores = await db.scores.find_one({"player_name": player_name})
    return {"player_name": player_scores["player_name"], "score": player_scores["score"]}