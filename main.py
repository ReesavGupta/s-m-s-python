from fastapi import FastAPI
from routers.student_router import router as student_router

app = FastAPI()

# Register the router
app.include_router(student_router, prefix="/students", tags=["Students"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Student Management System"}
