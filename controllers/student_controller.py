from fastapi import HTTPException
from models.student_model import Student
from db.conn import students_collection
from bson import ObjectId
from typing import Optional

# Helper function to format a MongoDB document before returning it
def format_student(student):
    """Format a MongoDB document before returning it as a response."""
    student["id"] = str(student["_id"])  # Convert ObjectId to a string
    del student["_id"]  # Remove the original _id field
    return student

async def create_student(student: Student):
    student_dict = student.model_dump(by_alias=True)

    print("Student Dict Before Insert:", student_dict) 

    try:
        result = await students_collection.insert_one(student_dict)
        print("\nInserted ID:", result.inserted_id)  
    except Exception as e:
        print("Error inserting student into database:", e)
        raise HTTPException(status_code=500, detail="Failed to insert student")

    formatted_result = format_student({"_id": result.inserted_id, **student_dict})

    return {"student": formatted_result}


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
        raise HTTPException(status_code=500, detail="Failed to list all students")

    return {"data": [format_student(student) for student in res_students]}
