# Audio and Sprite Management API

This FastAPI application provides a backend service for uploading, storing, and retrieving audio files and sprites (images) from a MongoDB database. It's designed to be deployed on Vercel.

## Features

- Upload sprite files (JPEG, PNG)
- Upload audio files (MP3, OGG)
- Store player scores
- Retrieve sprites by filename
- Retrieve audio files by filename
- Retrieve player scores by player name

## Prerequisites

- Python 3.8+
- MongoDB Atlas account
- Vercel account (for deployment)

## Local Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create a virtual environment

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root with your MongoDB connection string:

### 5. Run the application

```bash
uvicorn main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000)

## API Documentation

Once the server is running, access the interactive API documentation at:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Test endpoint returning a welcome message |
| `/upload_sprite` | POST | Upload a sprite image (JPEG, PNG) |
| `/upload_audio` | POST | Upload an audio file (MP3, OGG) |
| `/player_score` | POST | Add a player's score |
| `/get_sprite` | GET | Retrieve a sprite by name |
| `/get_audio_files` | GET | Retrieve an audio file by name |
| `/get_player_scores` | GET | Retrieve a player's scores by name |

## Deployment to Vercel

### 1. Install Vercel CLI

```bash
npm i -g vercel
```

### 2. Deploy

```bash
vercel
```

Follow the prompts to link your project to Vercel.

### 3. Configure Environment Variables

Add your `MONGO_URI` in the Vercel project settings.

## Project Structure

- `main.py`: Main application file containing all API endpoints
- `requirements.txt`: Python dependencies
- `vercel.json`: Vercel deployment configuration
- `.env`: Environment variables (not committed to version control)

## Troubleshooting

- If you encounter a "422 Unprocessable Content" error when uploading files, check that your client is correctly sending the file as `multipart/form-data`.
- For "UnicodeDecodeError" when retrieving files, ensure the file content is properly base64 encoded before storage and decoded after retrieval.
- Ensure your MongoDB connection string in the environment variables is correct and your network allows connections to MongoDB Atlas.
