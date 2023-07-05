import os
from databases import Database
from fastapi import FastAPI
from tracking.tracker import router as tracking_router
from logger import logging_config
from db.db_operations import connect_to_db, disconnect_from_db

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
    await connect_to_db(database)


@app.on_event("shutdown")
async def shutdown():
    """
    Disconnect from the database.
    This function is run when the FastAPI application shuts down.
    """
    await disconnect_from_db(database)


app.include_router(tracking_router)
