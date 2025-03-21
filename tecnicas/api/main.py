from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelos
class Employee(BaseModel):
    id: int
    name: str
    position: str
    department: str

class EmployeeCreate(BaseModel):
    name: str
    position: str
    department: str

# Base de datos en memoria
employees_db = [
    {"id": 1, "name": "Jon Done", "position": "Developer", "department": "IT"},
    {"id": 2, "name": "Steve Jobs", "position": "Designer", "department": "UX"}
]

# Configuración del router
employee_router = APIRouter(
    prefix="/employees",
    tags=["employees"]
)

@employee_router.get("/", response_model=List[Employee])
async def get_employees():
    return employees_db

@employee_router.post("/", response_model=Employee)
async def create_employee(employee: EmployeeCreate):
    new_id = len(employees_db) + 1
    new_employee = {
        "id": new_id,
        "name": employee.name,
        "position": employee.position,
        "department": employee.department
    }
    employees_db.append(new_employee)
    return new_employee

app.include_router(employee_router)