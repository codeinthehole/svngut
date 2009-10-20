from svngut import *
import datetime
import pysvn
import logging
import sys
import smtplib
from email.mime.text import MIMEText

# Set up logger
logging.basicConfig(
    stream = sys.stdout,  
    level = logging.INFO,
    format = "%(asctime)s\t%(message)s"
);
logging.info("Starting SVN gut - let the digestin' begin...")

# Import configuration
try:
    from config import svn_username, svn_password, repository_mapping, \
        user_repository_mapping, analysis_period_in_days, email_server, email_sender
    # Summarise configuration
    logging.info("Parsing config file...")
    logging.info("Config: found %d repo(s) to digest" % len(repository_mapping))
    logging.info("Config: found %d recipient(s) to inform" % len(user_repository_mapping.keys()))
except ImportError:
    logging.info("Cannot load configuration from config file (config.py)")
    sys.exit()

# Create repository mappings
repositories = {}
for name, url in repository_mapping.items():
    repositories[name] = SvnRepo(url, svn_username, svn_password)
user_repositories = {}
for user, repository_list in user_repository_mapping.items():
    user_repositories[user] = [repositories[name] for name in repository_list]

# Get date range for analysis
today = datetime.date.today()
start_date = datetime.datetime(today.year, today.month, today.day-analysis_period_in_days, 0, 0, 0)
end_date = datetime.datetime(today.year, today.month, today.day-1, 23, 59, 59)
date_range = (start_date, end_date)
logging.info("Date range: %s to %s (last %d days)" % \
        (start_date.strftime("%Y-%m-%d %H:%M"), end_date.strftime("%Y-%m-%d %H:%M"), analysis_period_in_days))

# Assign contributions to each repo
interrogator = SvnCommitRetriever(pysvn.Client())
repository_contributions = {}
for name, repo in repositories.items():
    contributors = interrogator.get_contributors(repo, date_range)
    repository_contributions[repo.url] = contributors

# Send notifications
logging.info("Sending notification emails...")
server = smtplib.SMTP(email_server)
for email_address, repository_list in user_repositories.items():
    logging.info(" - Sending summary of %d repo(s) to %s" % (len(repository_list), email_address))
    # Construct email body (need to refactor to use templating language)
    email_body = "<html>"
    for repo in repository_list:
        contributions = repository_contributions[repo.url]
        if (len(contributions) > 0): 
            email_body += "Repository: <strong>%s</strong>" % repo.url
            email_body += "<ol><li>"
            email_body += "</li><li>".join([contribution.get_email_summary() for contribution in contributions])
            email_body += "</li></ol>"
    email_body += "</html>"
    logging.info(email_body)

    message = MIMEText(email_body, 'html')
    message['Subject'] = 'SVNGUT summary for %s' % (start_date.strftime("%Y-%m-%d"))
    message['From'] = email_sender
    message['To'] = email_address
    server.sendmail(email_sender, [email_address], message.as_string())
server.quit()
logging.info("Finished SVN Gut")   