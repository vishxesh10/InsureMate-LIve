from pydantic import BaseModel, Field, EmailStr, AnyUrl, computed_field
from typing import List, Dict

class MyModel(BaseModel):
    name: str
    age: int
    height: float
    weight: float
    skills: List[str]
    contact: Dict[str, str]
    email: EmailStr
    linkedIn: AnyUrl

    @computed_field  # ✅ Pydantic v2 feature
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)


def Model(mymodel: MyModel):
    print("Name:", mymodel.name)
    print("Age:", mymodel.age)
    print("Skills:", mymodel.skills)
    print("Contact:", mymodel.contact)
    print("BMI:", mymodel.bmi)
    print("Email:", mymodel.email)
    print("LinkedIn:", mymodel.linkedIn)
    return mymodel  # ✅ Return karna better hai


info = {
    "name": "Vishesh",
    "age": 21,
    "height": 1.75,
    "weight": 70,
    "skills": ["Python", "FastAPI"],
    "contact": {"mobile": "8950151945", "emergency": "384738538"},
    "email": "vishesh23022005@hdfc.com",
    "linkedIn": "https://www.linkedin.com/in/vishesh10"  # ✅ valid URL
}

info1 = Model(MyModel(**info))
