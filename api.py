import os
from fastapi import APIRouter, FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio
from core.config import settings
from db.mongo_db import db_mongo as mongo_db
# from dotenv import load_dotenv
 
# BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# load_dotenv()
# app = FastAPI()
app =APIRouter(include_in_schema=True)
# client = motor.motor_asyncio.AsyncIOMotorClient(settings.)#os.environ['MONGODB_URI'])
# mongo_db = client.college


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class ContactModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    message: str =Field(...)
    class Config:
        # __tablename__ = 'contact'
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "message": "Experiments, Science, and Fashion in Nanophotonics",
           
            }
        }

class StudentModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    course: str = Field("")
    gpa: float = Field(3, le=4.0)
    
    class Config:
        
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": "3.0",
            }
        }
class UpdateStudentModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    course: Optional[str]
    gpa: Optional[float]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": "3.0",
            }
        }

@app.post("/contactsubmit",response_description='Add Contact',response_model=ContactModel)
async def submit_contact(contact : ContactModel= Body(...)):
    randomcontact=contact
    contactlist=[]
    # for i in range(100000):
    #     randomcontact.id= ObjectId ()
    #     print(randomcontact)
    #     contactd = jsonable_encoder(contact)
    #     contactlist.append(contactd)
    # new_contact = await mongo_db["contact"].insert_many(contactlist)
    contactd = jsonable_encoder(contact)
    new_contact = await mongo_db["contact"].insert_one(contactd)
    contactlist.append(contactd)
    # created_contact = await mongo_db["contact"].find_one({"_id": new_contact.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={})

@app.get("/contactslist",response_description='All Contacts',response_model=List[ContactModel])
async def list_contacts():
    contacts = await mongo_db["contact"].find().to_list(100)
    return contacts
@app.post("/apiapp", response_description="Add new student", response_model=StudentModel)
async def create_student(student: StudentModel = Body(...)):
    student = jsonable_encoder(student)
    new_student = await mongo_db["students"].insert_one(student)
    created_student = await mongo_db["students"].find_one({"_id": new_student.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)


@app.get(
    "/allstudents", response_description="List all students", response_model=List[StudentModel]
)
async def list_students():
    students = await mongo_db["students"].find().to_list(100)
    return students


@app.get(
    "/allstudents/{id}", response_description="Get a single student", response_model=StudentModel
)
async def show_student(id: str):
    if (student := await mongo_db["students"].find_one({"_id": id})) is not None:
        return student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.put("/allstudents/{id}", response_description="Update a student", response_model=StudentModel)
async def update_student(id: str, student: UpdateStudentModel = Body(...)):
    student = {k: v for k, v in student.dict().items() if v is not None}

    if len(student) >= 1:
        update_result = await mongo_db["students"].update_one({"_id": id}, {"$set": student})

        if update_result.modified_count == 1:
            if (
                updated_student := await mongo_db["students"].find_one({"_id": id})
            ) is not None:
                return updated_student

    if (existing_student := await mongo_db["students"].find_one({"_id": id})) is not None:
        return existing_student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.delete("/allstudents/{id}", response_description="Delete a student")
async def delete_student(id: str):
    delete_result = await mongo_db["students"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Student {id} not found")