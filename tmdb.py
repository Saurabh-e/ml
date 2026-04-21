import httpx
import os

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# 🔍 Search movie
async def search_movie(query: str):
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": query
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.get(url, params=params)
            data = response.json()
            return data.get("results", [])
        except Exception as e:
            print("TMDB ERROR:", e)
            return []

# 🎬 Format movie data
def format_movie(movie):
    return {
        "title": movie.get("title"),
        "overview": movie.get("overview"),
        "poster": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get("poster_path") else None,
        "rating": movie.get("vote_average"),
        "release_date": movie.get("release_date")
    }
