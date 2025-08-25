from pydantic import BaseModel, Field, EmailStr, AnyUrl, model_validator
from typing import List, Dict

class MyModel(BaseModel):
    name: str
    age: int
    skills: List[str]
    contact: Dict[str, str]
    email: EmailStr
    linkedIn: AnyUrl

    @model_validator(mode="after")
    def validate_age(cls, model):
        if model.age > 60 and 'emergency' not in model.contact:
            raise ValueError("Age above 60 requires emergency contact information.")
        return model


def Model(mymodel: MyModel):
    print(mymodel.name)
    print(mymodel.age)
    print(mymodel.skills)
    print(mymodel.contact)
    print(mymodel.email)
    print(mymodel.linkedIn)


info = {
    "name": "Vishesh",
    "age": 89,
    "skills": ["Python", "FastAPI"],
    "contact": {"mobile": "8950151945" , "emergency" : "384738538"},
    "email": "vishesh23022005@hdfc.com",
    "linkedIn": "https://www.linkedinsh2302/"
}

info1 = Model(MyModel(**info))
