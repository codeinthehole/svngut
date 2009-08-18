import smtplib

# Send emails
server = smtplib.SMTP('localhost')
server.sendmail('svngut@orwell.tangentlabs.co.uk', 'david.winterbottom@gmail.com', 'testing')
server.quit()