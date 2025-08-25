from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field , computed_field
from fastapi.responses import JSONResponse
from typing import Annotated,Optional,AnyStr
import json
import os

app = FastAPI()

class Student(BaseModel):
    id: Annotated[str, Field(description="ID of the student", example="S1001")]
    name: Annotated[str, Field(description="Name of the student", example="John Doe")]
    city: Annotated[str, Field(description="City of the student", example="New York")]
    age: Annotated[int, Field(description="Age of the student", example=20)]
    Gender: Annotated[str, Field(description="Gender of the student", example="male")]
    height: Annotated[float, Field(description="Height of the student in cm", example=170.5)]
    weight: Annotated[float, Field(description="Weight of the student in kg", example=70.0)]


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / ((self.height / 100) ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"



class Update_Student(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(gt=0,lt=120,default=None)]
    Gender:Annotated[Optional[str],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None,gt=0)]
    weight:Annotated[Optional[float],Field(default=None,gt=0)]
        

def load_data():
    if not os.path.exists("student.json"):   # agar file nahi hai toh empty dict
        return {}
    with open("student.json", "r") as f:
        return json.load(f)

def save_data(data):
    with open("student.json", "w") as f:
        json.dump(data, f, indent=4)

@app.get("/")
def home():
    return {"message": "My first Endpoint"}

@app.get("/view")
def view():
    data = load_data()
    return data



@app.post("/create")
def create_data(student: Student):
    # load
    data = load_data()

    # check
    if student.id in data:
        raise HTTPException(status_code=400, detail="Student already exists")

    # data enter krna hai (id ko alag rakha hai)
    data[student.id] = student.model_dump(exclude={"id"})

    # save the data
    save_data(data)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Student created successfully",
            "student": student.model_dump()
        }
    )



# @app.put("/update/{id}")
# def update_data(id: str, student: Update_Student):
#     # load
#     data = load_data()

#     # check (path ke id ke hisaab se check karo)
#     if id not in data:
#         raise HTTPException(status_code=404, detail="Student not found")

#     # update (path ke id pe overwrite karo, body ka id ignore kar do)
#     existing_data = data[id]
#     updated_info_student = student.model_dump(exclude_unset=True)

#     for key, value in updated_info_student.items():
#         existing_data[key] = value

#     #ye kam hum sirf bmi and verdict ke liye kar rahe hai, agr by chance height or weight update hua hai toh ye 2 field bhi change hoyengi
#     #2).Id add krenge model me
#     existing_data["id"] = student.id
#     #3).ab existing data ko model me dalke object bnao
#     #1) . pehle ek main model ka object bnao aur upated data usme dal do
#     student_obj = Student(**existing_data) #abhi ye object bnega hi nhi , kyuki isme ID field nhi hai toh humne ID add krni pdegi  


#     #4) ab is object se dobara dict me convert krdo
#     existing_data = student_obj.model_dump()



#     data[student.id] = existing_data
    

#     # save
#     save_data(data)

#     return JSONResponse(
#         status_code=200,
#         content={
#             "message": "Student updated successfully",
#             "student": {"id": id, **student.model_dump(exclude={"id"})}
#         }
#     )


@app.put("/update/{id}")
def update_data(id: str, student: Update_Student):
    data = load_data()

    if id not in data:
        raise HTTPException(status_code=404, detail="Student not found")

    existing_data = data[id]
    updated_info_student = student.model_dump(exclude_unset=True)

    # apply updates
    for key, value in updated_info_student.items():
        existing_data[key] = value

    # ensure id present
    existing_data["id"] = id

    # rebuild Student object to recalc bmi/verdict
    student_obj = Student(**existing_data)

    # update dictionary
    data[id] = student_obj.model_dump()

    # save
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Student updated successfully",
            "student": student_obj.model_dump()
        }
    )


@app.delete("/delete/{id}")
def delete_data(id: str):

    # load
    data = load_data()

    # check
    if id not in data:
        raise HTTPException(status_code=404, detail="Student not found")

    # delete
    del data[id]

    # save
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Student deleted successfully"
        }
    )