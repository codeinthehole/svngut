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
except ImportError:
    logging.info("Cannot find config file (config.py)")
    sys.exit()

# Summarise configuration
logging.info("Config: found %d repo(s) to digest" % len(repository_mapping))
logging.info("Config: found %d recipient(s) to inform" % len(user_repository_mapping.keys()))

# Create repository mappings
repositories = {}
for name, url in repository_mapping.items():
    repositories[name] = SvnRepo(url, svn_username, svn_password)

user_repositories = {}
for user, repository_list in user_repository_mapping.items():
    user_repositories[user] = [repositories[name] for name in repository_list]

# Get date range for analysis
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=analysis_period_in_days)
date_range = (start_date, end_date)
logging.info("Date range: %s to %s (last %d days)" % \
             (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), analysis_period_in_days))

interrogator = SvnCommitRetriever(pysvn.Client())
for name, repo in repositories.items():
    contributors = interrogator.get_contributors(repo, date_range)
    for contributor in contributors:
        print contributor.get_email_summary()
    



