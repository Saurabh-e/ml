from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from recommender import recommend
from tmdb import search_movie, format_movie

app = FastAPI(title="ML Movie Recommender")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HEALTH
@app.get("/")
def home():
    return {"status": "ML Service Running"}

# 🔍 SEARCH (TMDB MULTIPLE RESULTS)
@app.get("/search")
async def search(query: str):
    results = await search_movie(query)
    return [format_movie(m) for m in results[:10]]

# 🎯 RECOMMENDATIONS
@app.get("/recommend")
async def get_recommendations(
    title: str = Query(...),
    top_n: int = 10
):
    recs = recommend(title, top_n)

    output = []
    for r in recs:
        tmdb_data = await search_movie(r["title"])
        if tmdb_data:
            output.append(format_movie(tmdb_data[0]))

    return output

# 🏠 HOME (TRENDING MOCK)
@app.get("/home")
async def home_feed():
    movies = await search_movie("avengers")
    return [format_movie(m) for m in movies[:10]]