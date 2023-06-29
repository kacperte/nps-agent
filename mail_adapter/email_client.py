import datetime
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from databases import Database
from datetime import datetime

DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"
database = Database(DATABASE_URL)


class MailClient:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.server = aiosmtplib.SMTP(self.host, self.port, use_tls=True)

    async def login(self):
        try:
            await self.server.connect()
            await self.server.login(self.username, self.password)
        except aiosmtplib.SMTPException as e:
            print(f"Failed to login: {e}")
            raise

    async def send_mail(self, recipient_email: str, subject: str, content, project_name):
        await self.login()
        try:
            message = self._compose_message(content, recipient_email, subject)
            await self.server.send_message(message)
            await self.add_record_to_db(email_id=recipient_email, date=datetime.now(), projectname=project_name)
        except aiosmtplib.SMTPException as e:
            print(f"Failed to send email: {e}")
            raise
        finally:
            await self.server.quit()

    def _compose_message(self, content, recipient_email, subject):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.username
        message["To"] = recipient_email
        message.attach(MIMEText(content, "html"))

        return message

    @staticmethod
    async def add_record_to_db(email_id, date, projectname):
        query = "INSERT INTO sent_emails (email_id, date, project) VALUES (:email_id,:date, :project)"
        await database.execute(query=query, values={"email_id": email_id, "date": date, "project": projectname})
