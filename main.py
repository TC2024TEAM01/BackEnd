from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()





@app.get("/")
def reaf_root():
  return 'pdd'

