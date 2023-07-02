from asyncpg.exceptions import UniqueViolationError, DataError, UndefinedTableError
from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse
from databases import Database
from pydantic import BaseModel, EmailStr
import os

# Database connection string
DATABASE_URL = os.getenv("DATABASE_URL")
# Create a new database connection
database = Database(DATABASE_URL)

# Create a new FastAPI application
router = APIRouter(prefix="/track", tags=["tracking"])


# Define a Pydantic model for email data
class Email(BaseModel):
    email_id: EmailStr


# Register an email open event in the database
async def register_open(email: Email):
    # Check if the email exists in the sent_emails table
    query = "SELECT * FROM sent_emails WHERE email_id = :email_id"
    result = await database.fetch_one(query=query, values={"email_id": email.email_id})
    if result is None:
        # If the email does not exist, raise an HTTP 400 error
        raise HTTPException(status_code=400, detail="Email not found")
    # Insert a new record into the opens table
    query = "INSERT INTO opens (email_id) VALUES (:email_id)"
    await database.execute(query=query, values={"email_id": email.email_id})


# Connect to the database when the application starts
@router.on_event("startup")
async def startup():
    await database.connect()


# Disconnect from the database when the application shuts down
@router.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Define a new endpoint for tracking email opens
@router.get(
    path="/track/{email_id}",
    summary="Track Email Opens",
    description="This endpoint is used to track when an email sent to a user is opened. It works by embedding a 1x1 "
    "pixel image in the email. When the email client or web browser used to view the email requests the "
    "image, the GET request is logged as an 'open' event for that specific email. If the image file does "
    "not exist, a 500 error is returned.",
)
async def track(email_id: str):
    email = Email(email_id=email_id)
    try:
        # Register the email open event
        await register_open(email)
    except UniqueViolationError:
        raise HTTPException(status_code=400, detail="Email already registered")
    except DataError:
        raise HTTPException(status_code=400, detail="Invalid data")
    except UndefinedTableError:
        raise HTTPException(status_code=500, detail="Table does not exist")
    except Exception as e:
        # If any other error occurs, raise an HTTP 500 error with the error message
        raise HTTPException(status_code=500, detail=str(e))
    else:
        # If the tracking pixel image exists, return it as a response
        if os.path.exists("pixel.png"):
            return FileResponse("pixel.png", media_type="image/png")
        else:
            # If the tracking pixel image does not exist, raise an HTTP 500 error
            raise HTTPException(status_code=500, detail="Image file not found")
