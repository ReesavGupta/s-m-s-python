from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

from routers.student_router import router as student_router
app.include_router(student_router, prefix="/students", tags=["Students"])

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled exception: {exc}")

    return JSONResponse(
        status_code=500,
        content={"message": "An internal error occurred. Please try again later."},
    )

@app.get("/")
async def root():
    return {"message": "Welcome to the Student Management System"}
