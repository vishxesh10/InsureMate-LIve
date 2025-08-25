from pydantic import BaseModel, Field, EmailStr, AnyUrl,field_validator
from typing import List, Dict, Union,Annotated

class MyModel(BaseModel):
    name: str
    age: int
    skills: List[str]
    contact: Union[str, Dict[str, str]]  # Can be string or dict
    email: EmailStr
    linkedIn: AnyUrl


    @field_validator("email")
    @classmethod
    def validate_email(cls, value):

        valid_domains = ["hdfc.com", "icici.com", "axis.com"]
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError("Email domain must be one of the following: " + ", ".join(valid_domains))
        
        return value
    

    @field_validator("name")
    @classmethod
    def transform_name(cls, value):
        return value.upper()
                             



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
    "email": "vishesh23022005@hdfc.com",
    "linkedIn": "https://www.linkedinsh2302/"
}

info1 = Model(MyModel(**info))
