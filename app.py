from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field , computed_field
from typing import Literal,Annotated
import pickle
import pandas as pd


#step 1 : import the ml model
with open("model.pkl","rb") as f:
    model = pickle.load(f)

app = FastAPI()
# Tier 1 cities
tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]

# Tier 2 cities
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]


#pydantic model to valide the input data
class Userinput(BaseModel):
    age: Annotated[int , Field(...,gt=0,lt=120,description="Age of the person",example=25)]
    
    weight:Annotated[float, Field(...,gt=0,description="Weight of the person in kg",example=70.5)]
    
    height:Annotated[float, Field(...,gt=0,description="Height of the person in cm",example=175.5)]
    
    income_lpa:Annotated[float, Field(...,gt=0,description="Income of the person in LPA",example=5.5)]
    
    smoker:Annotated[bool, Field(...,description="Is the person a smoker?",example=False)]
    
    city:Annotated[str, Field(...,description="City of the person",example="New York")]
    
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(...,description="Occupation of the person",example="engineer")]
    

    @computed_field
    @property
    def bmi(self) -> float:
       return self.weight / ((self.height)**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
            if self.smoker and self.bmi > 30:
                return "high"
            elif self.smoker and self.bmi > 27:
                return "medium"
            else:
                return "low"
            
    @computed_field
    @property
    def age_group(self) ->str:
        if self.age<25:
            return "young"
        elif self.age<45:
            return "adult"
        elif self.age<60:
            return "middle-aged"
        else:
            return "senior"


    @computed_field
    @property   
    def city_tier(self) ->int:
       
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3  


@app.post("/predict")
def predict_premium(data:Userinput):
    input_df = pd.DataFrame([{
        "bmi": data.bmi,
        "lifestyle_risk": data.lifestyle_risk,
        "age_group": data.age_group,
        "city_tier": data.city_tier,
        "occupation": data.occupation,
        "income_lpa": data.income_lpa
    }])

       
       


    prediction = model.predict(input_df)[0]    

    return JSONResponse(content={"predicted_category": prediction})   