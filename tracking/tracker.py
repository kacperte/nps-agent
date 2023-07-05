from asyncpg.exceptions import UniqueViolationError, DataError, UndefinedTableError
from fastapi import APIRouter, HTTPException, Path
from starlette.responses import FileResponse
from databases import Database
from pydantic import BaseModel, EmailStr
import os
from db.db_operations import register_open, connect_to_db, disconnect_from_db

# Database connection string
DATABASE_URL = os.getenv("DATABASE_URL")
# Create a new database connection
database = Database(DATABASE_URL)

# Create a new FastAPI application
router = APIRouter(prefix="/track", tags=["tracking"])


# Connect to the database when the application starts
@router.on_event("startup")
async def startup():
    await connect_to_db(database)


# Disconnect from the database when the application shuts down
@router.on_event("shutdown")
async def shutdown():
    await disconnect_from_db(database)


# Define a new endpoint for tracking email opens
@router.get(
    path="/track/{email_id}",
    summary="Track Email Opens",
    description="This endpoint is used to track when an email sent to a user is opened. It works by embedding a 1x1 "
    "pixel image in the email. When the email client or web browser used to view the email requests the "
    "image, the GET request is logged as an 'open' event for that specific email. If the image file does "
    "not exist, a 500 error is returned.",
)
async def track(email_id: EmailStr = Path(...)):
    try:
        # Register the email open event
        await register_open(email_id, database)
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
