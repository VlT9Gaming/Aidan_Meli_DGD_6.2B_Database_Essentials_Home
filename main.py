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

# Define the FastAPI app
@app.get("/")
async def root():
    """
        Root endpoint that returns a welcome message. This is to test if the server is running.
    """
    return {"message": "Hello World"}

ALLOWED_SPRITE_TYPES = ["image/jpeg", "image/png", "image/jpg"]
ALLOWED_AUDIO_TYPES = ["audio/mpeg", "audio/ogg"]
@app.post("/upload_sprite")
async def upload_sprite(file: UploadFile = File(...), db=Depends(get_database)):
    """
        Endpoint to upload a sprite file.
        Validates the file type and stores the file content in the database.

        Args:
            file (UploadFile): The sprite file to upload.
            db: The database connection.

        Returns:
            dict: A message indicating the sprite was uploaded and the ID of the inserted document.
    """
    content = await file.read()
    if file.content_type not in ALLOWED_SPRITE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type for sprite")
    encoded_content = base64.b64encode(content).decode('utf-8')
    sprite_doc = {"filename": file.filename, "content": encoded_content}
    result = await db.sprites.insert_one(sprite_doc)
    return {"message": "Sprite uploaded", "id": str(result.inserted_id)}

@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...), db=Depends(get_database)):
    """
        Endpoint to upload an audio file.
        Validates the file type and stores the file content in the database.

        Args:
            file (UploadFile): The audio file to upload.
            db: The database connection.

        Returns:
            dict: A message indicating the audio file was uploaded and the ID of the inserted document.
    """
    content = await file.read()
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type for audio")
    encoded_content = base64.b64encode(content).decode('utf-8')
    audio_doc = {"filename": file.filename, "content": encoded_content}
    result = await db.audio.insert_one(audio_doc)
    return {"message": "Audio file uploaded", "id": str(result.inserted_id)}

@app.post("/player_score")
async def add_score(score: PlayerScore,db=Depends(get_database)):
    """
        Endpoint to add a player's score.
        Stores the player's name and score in the database.

        Args:
            score (PlayerScore): The player's score data.
            db: The database connection.

        Returns:
            dict: A message indicating the score was recorded and the ID of the inserted document.
    """
    score_doc = score.dict()
    result = await db.scores.insert_one(score_doc)
    return {"message": "Score recorded", "id": str(result.inserted_id)}

@app.get("/get_sprite")
async def get_sprites(sprite_name:str,db=Depends(get_database)):
    """
        Endpoint to retrieve a sprite file by its name.

        Args:
            sprite_name (str): The name of the sprite file to retrieve.
            db: The database connection.

        Returns:
            dict: The filename and content of the retrieved sprite file.
    """
    sprites = await db.sprites.find_one({"filename": sprite_name})
    return {"filename": sprites["filename"], "content": sprites["content"]}

@app.get("/get_audio_files")
async def get_audio_files(audio_name:str,db=Depends(get_database)):
    """
        Endpoint to retrieve an audio file by its name.

        Args:
            audio_name (str): The name of the audio file to retrieve.
            db: The database connection.

        Returns:
            dict: The filename and content of the retrieved audio file.
    """
    audio_files = await db.audio.find_one({"filename": audio_name})
    return {"filename": audio_files["filename"], "content": audio_files["content"]}


@app.get("/get_player_scores")
async def get_player_scores(player_name:str,db=Depends(get_database)):
    """
        Endpoint to retrieve a player's scores by their name.

        Args:
            player_name (str): The name of the player whose scores to retrieve.
            db: The database connection.

        Returns:
            dict: The player's name and their score.
    """
    player_scores = await db.scores.find_one({"player_name": player_name})
    return {"player_name": player_scores["player_name"], "score": player_scores["score"]}