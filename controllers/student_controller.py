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

    try:
        result = await students_collection.insert_one(student_dict)
        print("\nInserted ID:", result.inserted_id)  
    except Exception as e:
        print("Error inserting student into database:", e)
        raise HTTPException(status_code=500, detail="Failed to insert student")

    formatted_result = format_student({"_id": result.inserted_id, **student_dict})

    return {"id": str(result.inserted_id)}


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

async def fetch_student(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid student ID")

    student = await students_collection.find_one({"_id": ObjectId(id)})

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    no_id_student = format_student(student)
    no_id_student.pop("id")
    return no_id_student

async def update_student(id: str, update_data: dict):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid student ID")
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided to update")

    try:
        result = await students_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        
    except Exception as e:
        print("Error updating student:", e)
        raise HTTPException(status_code=500, detail="Failed to update student")
    
async def delete_student(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid student ID")
    
    try:
        result = await students_collection.delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        
        return {"message": "Student deleted successfully"}
    except Exception as e:
        print("Error deleting student:", e)
        raise HTTPException(status_code=500, detail="Failed to delete student")
