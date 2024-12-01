from fastapi import APIRouter, Query
from controllers.student_controller import create_student, list_students
from models.student_model import Student
from typing import Optional

router = APIRouter()

@router.post("/", status_code=201)
async def create_student_route(student: Student):
    return await create_student(student)

@router.get("/", status_code=200)
async def list_students_route(
    country: Optional[str] = Query(None, description="Filter by country"),
    age: Optional[int] = Query(None, description="Filter by minimum age")
):
    return await list_students(country=country, age=age)