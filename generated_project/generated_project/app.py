from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI Application"}

@app.post("/data")
async def create_data(data: dict):
    return {"message": "Data created successfully", "data": data}