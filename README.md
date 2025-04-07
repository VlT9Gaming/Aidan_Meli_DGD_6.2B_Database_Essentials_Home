# Multimedia Upload and Retrieval API

This project is a FastAPI-based application that allows users to upload and retrieve multimedia files (sprites and audio) and player scores. The files are stored in a MongoDB database.

## Setup

### Prerequisites

- Python 3.8 or higher
- MongoDB Atlas account
- Vercel account

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your MongoDB URI:
### Running the Application

1. Start the FastAPI server:

    ```sh
    uvicorn main:app --reload
    ```

2. The application will be available at `http://127.0.0.1:8000`.

### Deployment

1. Create a `vercel.json` file in the root directory with the following content:

    ```json
    {
     "version": 2,
     "builds": [
     {
     "src": "main.py",
     "use": "@vercel/python"
     }
     ],
     "routes": [
     {
     "src": "/(.*)",
     "dest": "main.py"
     }
     ]
    }
    ```

2. Deploy the application to Vercel:

    ```sh
    vercel
    ```

## API Endpoints

### Upload Sprite

- **URL:** `/upload_sprite`
- **Method:** `POST`
- **Request:**
  - `file`: The sprite file to upload (allowed types: `image/jpeg`, `image/png`, `image/jpg`)

### Upload Audio

- **URL:** `/upload_audio`
- **Method:** `POST`
- **Request:**
  - `file`: The audio file to upload (allowed types: `audio/mpeg`, `audio/ogg`)

### Add Player Score

- **URL:** `/player_score`
- **Method:** `POST`
- **Request:**
  - `player_name`: The name of the player
  - `score`: The score of the player

### Get Sprite

- **URL:** `/get_sprite`
- **Method:** `GET`
- **Request:**
  - `sprite_name`: The name of the sprite file to retrieve

### Get Audio Files

- **URL:** `/get_audio_files`
- **Method:** `GET`
- **Request:**
  - `audio_name`: The name of the audio file to retrieve

### Get Player Scores

- **URL:** `/get_player_scores`
- **Method:** `GET`
- **Request:**
  - `player_name`: The name of the player whose scores to retrieve

