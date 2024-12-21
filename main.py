from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()





@app.get("/")
def reaf_root():
  return 'pdd'
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

