from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello Python"}

@app.get("/employees/{employee_id}")
def read_employee(employee_id: int):
    return {
        "id": employee_id,
        "name": "wang",
        "salary": 8000
    }