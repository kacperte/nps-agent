import datetime
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from databases import Database
from datetime import datetime
import logging

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

    async def send_mail(
        self, recipient_email: str, subject: str, content, project_name
    ):
        """
        Send an email and record the event in the database.

        Args:
            recipient_email (str): The recipient's email address.
            subject (str): The email subject.
            content (str): The email content.
            project_name (str): The name of the project.

        Raises:
            aiosmtplib.SMTPException: If the email fails to send.
        """
        try:
            async with aiosmtplib.SMTP(self.host, self.port, use_tls=True) as server:
                await server.login(self.username, self.password)
                message = self._compose_message(content, recipient_email, subject)
                await server.send_message(message)
                await self.add_record_to_db(
                    email_id=recipient_email, date=datetime.now(), projectname=project_name
                )
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

    async def add_record_to_db(self, email_id, date, projectname):
        """
        Add a record to the sent_emails table in the database.

        Args:
            email_id (str): The email ID.
            date (datetime): The date the email was sent.
            projectname (str): The name of the project.
        """
        query = "INSERT INTO sent_emails (email_id, date, project) VALUES (:email_id,:date, :project)"
        await self.database.execute(
            query=query,
            values={"email_id": email_id, "date": date, "project": projectname},
        )
