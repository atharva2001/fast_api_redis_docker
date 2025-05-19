from fastapi import FastAPI 
import redis.client
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import requests
import json 
import redis
import logging

app = FastAPI(title="FastAPI with CORS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    filename="logs/app.log",  # log file inside container
    format="%(asctime)s - %(levelname)s - %(message)s",
)

redis_client = redis.Redis(
    host="redis",
    port=6379,
    db=0,
)

@app.get("/")
async def read_root():
    logging.info("Root endpoint accessed")
    return {"message": "Hello, World!"}

@app.get("/todos/{id}")
async def get_data(id: str):
    cache = redis_client.get(id)
    if cache:
        logging.info(f"Cache hit for ID: {id}")
        return json.loads(cache)
    else:
        logging.info(f"Cache miss for ID: {id}")
        res = requests.get(f"https://jsonplaceholder.typicode.com/todos/{id}")
        redis_client.set(id, res.text)
        return res.json()
    
@app.get("/todos")
async def get_all_data():
    cache = redis_client.get("all_todos")
    if cache:
        logging.info("Cache hit for all todos")
        return json.loads(cache)
    else:
        logging.info("Cache miss for all todos")
        res = requests.get("https://jsonplaceholder.typicode.com/todos")
        redis_client.set("all_todos", res.text)
        return res.json()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )