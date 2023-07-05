from databases import Database
from fastapi import HTTPException
from pydantic import EmailStr


async def connect_to_db(database: Database):
    """
    Connect to the database.

    Args:
        database (Database): The database connection instance.
    """
    await database.connect()


async def disconnect_from_db(database: Database):
    """
    Disconnect from the database.

    Args:
        database (Database): The database connection instance.
    """
    await database.disconnect()


async def register_open(email_id: EmailStr, database: Database):
    """
    Register an email open event in the database.

    Args:
        email_id (EmailStr): The email ID.
        database (Database): The database connection instance.

    Raises:
        HTTPException: If the email does not exist in the sent_emails table.
    """
    # Check if the email exists in the sent_emails table
    query = "SELECT * FROM sent_emails WHERE email_id = :email_id"
    result = await database.fetch_one(query=query, values={"email_id": email_id})
    if result is None:
        # If the email does not exist, raise an HTTP 400 error
        raise HTTPException(status_code=400, detail="Email not found")
    # Insert a new record into the opens table
    query = "INSERT INTO opens (email_id) VALUES (:email_id)"
    await database.execute(query=query, values={"email_id": email_id})


async def add_record_to_db(email_id, date, projectname, database: Database):
    """
    Add a record to the sent_emails table in the database.

    Args:
        email_id (str): The email ID.
        date (datetime): The date the email was sent.
        projectname (str): The name of the project.
        database (Database): The database connection instance.
    """
    query = "INSERT INTO sent_emails (email_id, date, project) VALUES (:email_id,:date, :project)"
    await database.execute(
        query=query,
        values={"email_id": email_id, "date": date, "project": projectname},
    )


