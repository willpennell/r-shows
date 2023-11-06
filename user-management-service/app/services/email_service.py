import smtplib
from app.config import MAILTRAP_PASSWORD, MAILTRAP_PORT, MAILTRAP_SERVER, MAILTRAP_USERNAME
from email.mime.text import MIMEText
from loguru import logger as log

class EmailService:
    def __init__(self):
        self.smtp_server: str = MAILTRAP_SERVER
        self.smtp_port: int = MAILTRAP_PORT
        self.smtp_username: str = MAILTRAP_USERNAME
        self.smtp_password: str = MAILTRAP_PASSWORD
        
    
    def send_email(self, email: str, content: str, subject: str):
        log.info("In send_email")
        sender = "Private Person <from@example.com>"
        receiver = f"A Test User <{email}>"

        message = MIMEText(content)
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = receiver

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            log.info("In Mailtrap Server")
            server.login(self.smtp_username, self.smtp_password)
            server.sendmail(sender, receiver, message.as_string())
            
    @staticmethod
    def reset_message(reset_token: str) -> str:
        return f"this is your link: http://localhost:8000/password/confirm?token={reset_token}"
    
    @staticmethod
    def activate_message(activate_token: str) -> str:
        return f"follow link to activate account http://localhost:8000/activate?token={activate_token}"

