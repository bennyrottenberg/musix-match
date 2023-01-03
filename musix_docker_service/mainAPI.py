#from queue import Empty

from musixAPI import Musix, MusixAPI
from fastapi import FastAPI, HTTPException,status

app = FastAPI(title="MusixLyricsGetter")

@app.post("/lyrics", status_code=status.HTTP_200_OK)
async def get_lyrics(musix_api: MusixAPI):
    """Musix Api get lyrics"""
    musix = Musix(musix_api=musix_api)
    try:
        response = musix.run()
        return response
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {err}",
        )
