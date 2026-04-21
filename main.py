from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from recommender import recommend
from tmdb import search_movie, format_movie
import asyncio

app = FastAPI(title="ML Movie Recommender API")

# ✅ CORS (allow all for Android/Web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root (health check)
@app.get("/")
def home():
    return {"status": "ML Service Running 🚀"}

# 🔍 SEARCH MOVIES FROM TMDB
@app.get("/search")
async def search(query: str):
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    results = await search_movie(query)
    return [format_movie(m) for m in results[:10]]

# 🎯 GET RECOMMENDATIONS
@app.get("/recommend")
async def get_recommendations(
    title: str = Query(...),
    top_n: int = 10
):
    try:
        recs = recommend(title, top_n)

        if not recs:
            return {"message": "Movie not found", "results": []}

        # ⚡ Run TMDB calls in parallel
        tasks = [search_movie(r["title"]) for r in recs]
        tmdb_results = await asyncio.gather(*tasks)

        output = []
        for res in tmdb_results:
            if res:
                output.append(format_movie(res[0]))

        return {"results": output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 🏠 HOME (TRENDING / DEFAULT)
@app.get("/home")
async def home_feed():
    movies = await search_movie("avengers")
    return [format_movie(m) for m in movies[:10]]

# 🧪 DEBUG ROUTE (optional)
@app.get("/test")
def test():
    return recommend("batman", 5)
