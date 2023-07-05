import os
from databases import Database
from fastapi import FastAPI
from tracking.tracker import router as tracking_router
from logger import logging_config

# This will configure logging for the entire application
logging_config.configure_logging()

DATABASE_URL = os.getenv("DATABASE_URL")
database = Database(DATABASE_URL)

app = FastAPI()


@app.on_event("startup")
async def startup():
    """
    Connect to the database.
    This function is run when the FastAPI application starts.
    """
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """
    Disconnect from the database.
    This function is run when the FastAPI application shuts down.
    """
    await database.disconnect()


app.include_router(tracking_router)
