import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE = "https://api.themoviedb.org/3"
IMG = "https://image.tmdb.org/t/p/w500"

async def search_movie(query):
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{BASE}/search/movie",
            params={"api_key": API_KEY, "query": query}
        )
        data = res.json()
        return data.get("results", [])

def format_movie(m):
    return {
        "tmdb_id": m["id"],
        "title": m.get("title"),
        "poster_url": IMG + m["poster_path"] if m.get("poster_path") else None,
        "rating": m.get("vote_average"),
        "release_date": m.get("release_date"),
    }