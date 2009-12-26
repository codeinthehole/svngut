import smtplib
import logging
from email.mime.text import MIMEText

class Notifier(object):
    
    def send_emails(self):
        logging.info("Sending notification emails...")
        pass
    
    def _tmp(self):
        
        server = smtplib.SMTP(email_server)
        message = MIMEText(email_body, 'html')
        message['Subject'] = 'SVNGUT summary for %s' % (start_date.strftime("%Y-%m-%d"))
        message['From'] = email_sender
        message['To'] = email_address
        server.sendmail(email_sender, [email_address], message.as_string())
        server.quit()