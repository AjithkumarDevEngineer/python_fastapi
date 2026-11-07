from fastapi import FastAPI
from .decorators import my_decoration

app = FastAPI()

@app.get("/")
@my_decoration
def home():
    print("Plain pizza is ready!")
    return {"message": "Plain pizza is ready! Hello FastAPI!"}