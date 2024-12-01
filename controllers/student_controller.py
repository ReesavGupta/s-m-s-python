from fastapi import HTTPException
from models.student_model import Student
from db.conn import students_collection
from bson import ObjectId
from typing import Optional
import configparser
from pathlib import Path

# Set up the path to the messages.properties file
base_path = Path(__file__).resolve().parent
config_path = base_path.parent / 'messages.properties'

config = configparser.ConfigParser()
config.read(config_path)

# Helper function to format a MongoDB document before returning it
def format_student(student):
    student["id"] = str(student["_id"])  # Convert ObjectId to a string
    del student["_id"]  # Remove the original _id field
    return student

# Create a new student
async def create_student(student: Student):
    student_dict = student.model_dump(by_alias=True)

    try:
        result = await students_collection.insert_one(student_dict)
        print("\nInserted ID:", result.inserted_id)  
    except Exception as e:
        print("Error inserting student into database:", e)
        raise HTTPException(
            status_code=500,
            detail=config.get('DEFAULT', 'student.create.fail')
        )

    return {"id": str(result.inserted_id)}

# List students with optional filters
async def list_students(country: Optional[str] = None, age: Optional[int] = None):
    query = {}
    
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}  

    print("\nthis is the query:", query)

    try:
        res_students = await students_collection.find(query).to_list(100)
    except Exception as e:
        print('Error getting back all the records:', e)
        raise HTTPException(
            status_code=500,
            detail=config.get('DEFAULT', 'student.list.fail')
        )

    return {"data": [format_student(student) for student in res_students]}

# Fetch a single student by ID
async def fetch_student(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=400,
            detail=config.get('DEFAULT', 'student.id.invalid')
        )

    student = await students_collection.find_one({"_id": ObjectId(id)})

    if not student:
        raise HTTPException(
            status_code=404,
            detail=config.get('DEFAULT', 'student.id.not_found')
        )

    formatted_student = format_student(student)
    return formatted_student

# Update a student by ID
async def update_student(id: str, update_data: dict):
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=400,
            detail=config.get('DEFAULT', 'student.id.invalid')
        )
    
    if not update_data:
        raise HTTPException(
            status_code=400,
            detail=config.get('DEFAULT', 'student.update.no_data')
        )

    try:
        result = await students_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=404,
                detail=config.get('DEFAULT', 'student.id.not_found')
            )
        
        return {"message": config.get('DEFAULT', 'student.update.success')}
    except Exception as e:
        print("Error updating student:", e)
        raise HTTPException(
            status_code=500,
            detail=config.get('DEFAULT', 'student.update.fail')
        )

# Delete a student by ID
async def delete_student(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=400,
            detail=config.get('DEFAULT', 'student.id.invalid')
        )
    
    try:
        result = await students_collection.delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail=config.get('DEFAULT', 'student.id.not_found')
            )
        
        return {"message": config.get('DEFAULT', 'student.delete.success')}
    except Exception as e:
        print("Error deleting student:", e)
        raise HTTPException(
            status_code=500,
            detail=config.get('DEFAULT', 'student.delete.fail')
        )
