from pydantic import BaseModel,EmailStr
from typing import List



class Contact(BaseModel):
    mobile: str
    emergency: str

class Address(BaseModel):
    city: str
    state: str
    country: str

class Student(BaseModel):
    name: str
    age: int
    email: EmailStr
    contact : Contact
    address : Address
    subjects: List[str]

data = {
    "name": "Vishesh",
    "age": 21,
    "email":"vishesh@gmail.com",
    "subjects": ["Python", "FastAPI"],
    "contact":{"mobile": "8950151945", "emergency": "384738538"},
    "address": {"city": "Delhi", "state": "Delhi", "country": "India"}
}

student = Student(**data)




temp = student.model_dump(include=["name"])
print(temp)
print(type(temp))
