import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
import motor.motor_asyncio

app = FastAPI()
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

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
async def upload_sprite(file: UploadFile = File(...),db=Depends(get_database)):
    # In a real application, the file should be saved to a storage service
    content = await file.read()
    sprite_doc = {"filename": file.filename, "content": content}
    result = await db.sprites.insert_one(sprite_doc)
    return {"message": "Sprite uploaded", "id": str(result.inserted_id)}

@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...),db=Depends(get_database)):
    content = await file.read()
    audio_doc = {"filename": file.filename, "content": content}
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
    return {"filename": sprites["filename"]}

@app.get("/get_audio_files")
async def get_audio_files(audio_name:str,db=Depends(get_database)):
    audio_files = await db.audio.find_one({"filename": audio_name})
    return {"filename": audio_files["filename"]}

@app.get("/get_player_scores")
async def get_player_scores(player_name:str,db=Depends(get_database)):
    player_scores = await db.scores.find_one({"player_name": player_name})
    return {"player_name": player_scores["player_name"], "score": player_scores["score"]}