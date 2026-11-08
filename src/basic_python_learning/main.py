from fastapi import FastAPI, Body, Form, UploadFile, File, HTTPException
from .decorators import my_decoration
from .pydantic_basics import Person
from .async_await import get_products_sync, get_products_async

app = FastAPI()

# GET API
@app.get("/")
@my_decoration
def home():
    print("Plain pizza is ready!")
    return {"message": "Plain pizza is ready! Hello FastAPI!"}

# Path "/person" GET API 
@app.get("/person")
def person(name: str | None = None,
    age: int | None = None,
    email: str | None = None):

    person_data = Person(
        **{
            key: value
            for key, value in {
                "name": name,
                "age": age,
                "email": email
            }.items()
            if value is not None
        }
    )

    return person_data

# POST API
@app.post("/add-person")
def receive_json(name: str | None = None,
    age: int | None = None,
    email: str | None = None):
    return {
        "type": "JSON",
        "name": name,
        "age": age,
        "email":email
    }
# media type - text/plain
@app.post("/text")
def receive_text(content: str = Body(..., media_type="text/plain")): # Mandotory field mentioned "..." ,  Optional give "none"
    return {
        "type": "Plain Text",
        "content": content
    }

# Form
@app.post("/form")
def formField(username:str= Form(...), password:str= Form(...)):
     return {
            "type": "Form Data",
            "username": username,
            "password":password
        }

# upload
@app.post("/upload")
def upload_file(file:UploadFile= File(...)):
     return {
            "type": "File Upload",
            "filename": file.filename,
            "content_type":file.content_type
        }

# Sync
# TEST_URL = "https://fakestoreapi.com/products/"
# TEST_URL = "https://official-joke-api.appspot.com/random_joke"
TEST_URL = "https://jsonplaceholder.typicode.com/posts/"

@app.get("/sync-product")
def get_products():
    try:
        return get_products_sync(TEST_URL)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/async-product")
async def get_async():
    try:
        return await get_products_async(TEST_URL)  
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
                    status_code=500,
                    detail=str(e)
                )
    