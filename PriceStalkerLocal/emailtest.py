# Import smtplib for the actual sending function
import smtplib
import time

# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.

# me == the sender's email address
# you == the recipient's email address
class email_handling:
    def __init__(self):
        self.server = smtplib.SMTP('smtp.gmail.com',587)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login('pricestalker1@gmail.com','price46@Stalker')
    
    def send_email(self, to_email, msg):
        self.server.sendmail('pricestalker1@gmail.com',to_email,msg)
