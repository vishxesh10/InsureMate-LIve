from pydantic import BaseModel, Field, EmailStr, AnyUrl
from typing import List, Dict, Union,Annotated

class MyModel(BaseModel):
    name: Annotated[str , Field(min_length=3, max_length=50, description="Name of the person" , example="Vishesh")]
    age: int
    skills: List[str]
    contact: Union[str, Dict[str, str]]  # Can be string or dict
    email: EmailStr
    linkedIn: AnyUrl


def Model(mymodel: MyModel):
    print(mymodel.name)
    print(mymodel.age)
    print(mymodel.skills)
    print(mymodel.contact)


info = {
    "name": "Vishesh",
    "age": 25,
    "skills": ["Python", "FastAPI"],
    "contact": "8950151945",  
    "email": "vishesh23022005@gmail.com",
    "linkedIn": "https://www.linkedinsh2302/"
}

info1 = Model(MyModel(**info))
