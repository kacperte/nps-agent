from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse
from databases import Database
from pydantic import BaseModel, EmailStr
import os

DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"
database = Database(DATABASE_URL)

app = FastAPI()


class Email(BaseModel):
    email_id: EmailStr


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


async def register_open(email: Email):
    query = "SELECT * FROM sent_emails WHERE email_id = :email_id"
    result = await database.fetch_one(query=query, values={"email_id": email.email_id})
    if result is None:
        raise HTTPException(status_code=400, detail="Email not found")
    query = "INSERT INTO opens (email_id) VALUES (:email_id)"
    await database.execute(query=query, values={"email_id": email.email_id})


@app.get("/track/{email_id}")
async def track(email_id: Email):
    try:
        await register_open(email_id)
        if os.path.exists("pixel.png"):
            return FileResponse("pixel.png", media_type="image/png")
        else:
            raise HTTPException(status_code=500, detail="Image file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
