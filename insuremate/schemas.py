"""
Pydantic models for InsureMate Insurance Premium Prediction System
"""

from pydantic import BaseModel, computed_field
from typing import Literal, Optional
from datetime import datetime


class Userinput(BaseModel):
    """Model for user input data to predict insurance premium"""
    age: int
    weight: float
    height: float
    income_lpa: float
    smoker: bool
    city: str
    occupation: Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job']
    
    class Config:
        validate_assignment = True
    
    def __init__(self, **data):
        super().__init__(**data)
        # Validate that height and weight are positive
        if self.height <= 0:
            raise ValueError("Height must be greater than 0")
        if self.weight <= 0:
            raise ValueError("Weight must be greater than 0")
        # Enforce minimum age for insurance applicants
        if self.age < 18 or self.age >= 120:
            raise ValueError("Age must be between 18 and 119")
        if self.income_lpa <= 0:
            raise ValueError("Income must be greater than 0")
    
    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate BMI from weight (kg) and height (cm)"""
        return self.weight / ((self.height)**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        """Determine lifestyle risk based on smoking and BMI"""
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker and self.bmi > 27:
            return "medium"
        else:
            return "low"
    
    @computed_field
    @property
    def age_group(self) -> str:
        """Categorize age into groups"""
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle-aged"
        else:
            return "senior"
    
    @computed_field
    @property   
    def city_tier(self) -> int:
        """Determine city tier based on city classification"""
        tier_1 = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
        tier_2 = [
            "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
            "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
            "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
            "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
            "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
            "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
        ]
        
        if self.city in tier_1:
            return 1
        elif self.city in tier_2:
            return 2
        else:
            return 3


class PredictionResponse(BaseModel):
    """Model for prediction response"""
    predicted_category: str
    result_id: int
    message: str
    explain_text: Optional[str] = None
    warnings: list[str] = []


class PredictionResultSchema(BaseModel):
    """Schema for prediction result retrieved from database"""
    id: int
    age: int
    weight: float
    height: float
    income_lpa: float
    smoker: bool
    city: str
    occupation: str
    bmi: float
    lifestyle_risk: str
    age_group: str
    city_tier: int
    predicted_category: str
    created_at: str
    
    class Config:
        from_attributes = True


class ResultsResponse(BaseModel):
    """Model for results endpoint response"""
    total_results: int
    results: list[PredictionResultSchema]


class ResultsByCityResponse(BaseModel):
    """Model for city-filtered results response"""
    city: str
    total_results: int
    results: list[PredictionResultSchema]


class ResultsByCategoryResponse(BaseModel):
    """Model for category-filtered results response"""
    category: str
    total_results: int
    results: list[PredictionResultSchema]
