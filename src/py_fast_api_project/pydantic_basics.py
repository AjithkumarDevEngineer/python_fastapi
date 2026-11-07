from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    email: str

valid_data = Person(name="ajith", age=30, email="ak@gmail.com")
print(valid_data)