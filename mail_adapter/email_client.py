import datetime
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from databases import Database
from datetime import datetime
import logging
from pydantic import ValidationError
from db.models import EmailData
from db.db_operations import add_record_to_db

# Get the logger for this module
logger = logging.getLogger(__name__)


class MailClient:
    def __init__(
        self, host: str, port: int, username: str, password: str, database_url: str
    ):
        """
        Initialize a new instance of the MailClient class.

        Args:
            host (str): The SMTP server host.
            port (int): The SMTP server port.
            username (str): The SMTP server username.
            password (str): The SMTP server password.
            database_url (str): The database connection string.
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = Database(database_url)

    async def send_mail(self, email_data: EmailData):
        """
        Send an email and record the event in the database.

        Args:
            email_data (EmailData): The email data.

        Raises:
            aiosmtplib.SMTPException: If the email fails to send.
            ValidationError: If the email data is invalid.
        """
        try:
            async with aiosmtplib.SMTP(self.host, self.port, use_tls=True) as server:
                await server.login(self.username, self.password)
                message = self._compose_message(
                    email_data.content, email_data.recipient_email, email_data.subject
                )
                await server.send_message(message)
                await add_record_to_db(
                    email_id=email_data.recipient_email,
                    date=datetime.now(),
                    projectname=email_data.project_name,
                    datebase=self.database
                )
        except ValidationError as e:
            logger.error(f"Invalid email data: {e}")
            raise
        except aiosmtplib.SMTPException as e:
            logger.error(f"Failed to send email: {e}")
            raise

    def _compose_message(self, content, recipient_email, subject):
        """
        Compose an email message.

        Args:
            content (str): The email content.
            recipient_email (str): The recipient's email address.
            subject (str): The email subject.

        Returns:
            MIMEMultipart: The composed email message.
        """
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.username
        message["To"] = recipient_email
        message.attach(MIMEText(content, "html"))

        return message

