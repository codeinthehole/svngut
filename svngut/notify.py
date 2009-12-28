import logging
from email.mime.text import MIMEText

class Notifier(object):
    
    def __init__(self, server, sender_address):
        self.server = server
        self.sender_address = sender_address
    
    def send_emails(self, recipient_address, message_html):
        logging.info("Sending notification email to %s..." % recipient_address)
        message = self._get_message(recipient_address, message_html)
        self.server.sendmail(self.sender_address, [recipient_address], message)
        self.server.quit()
    
    def _get_message(self, recipient_address, message_html):
        message = MIMEText(message_html, 'html')
        message['Subject'] = self._get_subject()
        message['From'] = self.sender_address
        message['To'] = recipient_address
        return message.as_string()
    
    def _get_subject(self):
        return 'SVNGUT' 
