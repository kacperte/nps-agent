from fastapi import FastAPI
from mail_adapter.email_client import MailClient
from tracking.tracker import app as tracking_app
from databases import Database

DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"
database = Database(DATABASE_URL)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()
    query = """
        CREATE TABLE IF NOT EXISTS sent_emails(
            email_id VARCHAR(255) NOT NULL,
            date TIMESTAMP WITH TIME ZONE NOT NULL,
            project VARCHAR(255) NOT NULL  
        );
    """
    await database.execute(query=query)
    query = """
        CREATE TABLE IF NOT EXISTS opens(
            email_id VARCHAR(255) NOT NULL,
            date TIMESTAMP WITH TIME ZONE NOT NULL,
            project VARCHAR(255) NOT NULL  
        );
    """
    await database.execute(query=query)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(tracking_app)


