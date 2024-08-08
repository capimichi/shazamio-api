import os
import tempfile

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
import asyncio
from shazamio import Shazam
import io
import uvicorn

class Track(BaseModel):
    track: str

app = FastAPI()

@app.post("/recognize")
async def recognize_song(track: Track):
    try:
        song_data = base64.b64decode(track.track)

        song_path = tempfile.mktemp()
        with open(song_path, 'wb') as f:
            f.write(song_data)

        shazam = Shazam()
        data = await shazam.recognize(song_path)

        # remove the temporary file
        os.remove(song_path)

        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)