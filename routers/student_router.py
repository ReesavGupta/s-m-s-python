from fastapi import APIRouter, Query, Path, Body
from controllers.student_controller import create_student, list_students, fetch_student, update_student
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

@router.get("/{id}", status_code=200)
async def fetch_student_route(id: str):
    return await fetch_student(id=id)

@router.patch("/{id}", status_code=204)
async def update_student_route(
    id: str = Path(..., description="The ID of the student to update"),
    update_data: dict = Body(..., description="The fields to update"),
):
    return await update_student(id, update_data)