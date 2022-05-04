from fastapi import FastAPI
import uvicorn
from cleaning import df,handler
from fuzzywuzzy import fuzz

allMovies = [movie for movie in df['title'] if str(movie) != 'nan']
print(allMovies)
app = FastAPI()


@app.get("/get-initial-recommendation/{movie_name}", )
async def get_initial_recommendation(movie_name : str ):


    # corrected name 
    ratio = {}
    for actual_name in allMovies:
        if actual_name != "": 
            ratio[actual_name] = fuzz.ratio(actual_name, movie_name)
    actual_name = sorted(ratio.items(), key=lambda x:x[1])[-1][0]

    if ratio[actual_name] < 60: 
        return {"status": "not found"}

    recommndation_list = [handler.get(i).name for i in handler.get(actual_name).adjList]
    return {"actual_name": actual_name , "recommendation_list": recommndation_list}






@app.get("/hello")
async def home():
    return {"hello": "world"}


if __name__=="__main__":
    uvicorn.run("server:app", host="0.0.0.0", reload=True, port=8000)
