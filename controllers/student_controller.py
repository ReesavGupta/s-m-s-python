from fastapi import HTTPException
from models.student_model import Student
from db.conn import students_collection
from bson import ObjectId

# Helper function to format a MongoDB document before returning it
def format_student(student):
    """Format a MongoDB document before returning it as a response."""
    student["id"] = str(student["_id"])  # Convert ObjectId to a string
    del student["_id"]  # Remove the original _id field
    return student

async def create_student(student: Student):
    # Convert the Pydantic model to a dictionary with field aliases
    student_dict = student.model_dump(by_alias=True)

    print("Student Dict Before Insert:", student_dict)  # Debugging statement

    # Convert the `id` field to MongoDB `_id` if provided
    if "id" in student_dict and student_dict["id"] is not None:
        try:
            student_dict["_id"] = ObjectId(student_dict.pop("id"))
        except Exception as e:
            print("Error converting id to ObjectId:", e)
            raise HTTPException(status_code=400, detail="Invalid ID format")

    # Insert the student document into MongoDB
    try:
        student_dict.pop("_id")
        result = await students_collection.insert_one(student_dict)
        print("\nInserted ID:", result.inserted_id)  # Debugging statement
    except Exception as e:
        print("Error inserting student into database:", e)
        raise HTTPException(status_code=500, detail="Failed to insert student")

    # Format the result before returning it
    formatted_result = format_student({"_id": result.inserted_id, **student_dict})

    # Return the formatted result
    return {"student": formatted_result}
