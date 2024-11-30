from fastapi import APIRouter
from controllers.student_controller import create_student
from models.student_model import Student

router = APIRouter()

@router.post("/", status_code=201)
async def create_student_route(student: Student):
    return await create_student(student)
