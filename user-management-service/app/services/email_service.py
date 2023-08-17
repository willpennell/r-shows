import smtplib
from app.config import MAILTRAP_PASSWORD, MAILTRAP_PORT, MAILTRAP_SERVER, MAILTRAP_USERNAME
from email.mime.text import MIMEText
from loguru import logger as log

class EmailService:
    def __init__(self):
        self.smtp_server = MAILTRAP_SERVER
        self.smtp_port = MAILTRAP_PORT
        self.smtp_username = MAILTRAP_USERNAME
        self.smtp_password = MAILTRAP_PASSWORD
        
    
    def send_email(self, email, reset_token):
        log.info("In send_email")
        sender = "Private Person <from@example.com>"
        receiver = f"A Test User <{email}>"
        
        content = f"this is your link: http://localhost:8000/password/confirm?token={reset_token}"

        message = MIMEText(content)
        message["Subject"] = "Reset Token"
        message["From"] = sender
        message["To"] = receiver

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            log.info("In Mailtrap Server")
            server.login(self.smtp_username, self.smtp_password)
            server.sendmail(sender, receiver, message.as_string())





