import smtplib
from app.config import MAILTRAP_PASSWORD, MAILTRAP_PORT, MAILTRAP_SERVER, MAILTRAP_USERNAME

class EmailService:
    def __init__(self):
        self.smtp_server = MAILTRAP_SERVER
        self.smtp_port = MAILTRAP_PORT
        self.smtp_username = MAILTRAP_USERNAME
        self.smtp_password = MAILTRAP_PASSWORD
        
    
    def send_email(self, email, reset_token):
        
        sender = "Private Person <from@example.com>"
        receiver = f"A Test User <{email}>"
        
        full_message = f"""\
                        Subject: Hi Mailtrap
                        To: {receiver}
                        From: {sender}

                        Reset Token: {reset_token}
                        
                        Regards,
                        R-shows 
                        """
        
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.login(self.smtp_username, self.smtp_password)
            server.sendmail(sender, receiver, full_message)





