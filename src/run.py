from svn.repo import *
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
    repositories[name] = Repo(url, svn_username, svn_password)

user_repositories = {}
for user, repository_list in user_repository_mapping.items():
    user_repositories[user] = [repositories[name] for name in repository_list]

# Get date range for analysis
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=analysis_period_in_days)
date_range = (start_date, end_date)
logging.info("Date range: %s to %s (last %d days)" % \
             (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), analysis_period_in_days))

# Analyse commits into hash
svn_interrogator = CommitRetriever(pysvn.Client())
commit_analyser = CommitSummariser()
repository_summaries = {}
for name, repository in repositories.items():
    logging.info("Checking repo: %s" % repository.url)
    try:
        commits = svn_interrogator.get_commits_for_date_range(repository, date_range)
        logging.info("Found %d commits" % len(commits))
        summary = commit_analyser.get_commit_list_summary(commits)
        for user, info in summary.items():
            logging.info(" - %s\t%d commits" % (user.ljust(20), info["commits"]))
        repository_summaries[repository.url] = summary
    except pysvn._pysvn.ClientError:
        logging.info("SVN client error - cannot access %s" % repository.url)
    
print repository_summaries    
    
# Send notifications
logging.info("Sending emails...")
server = smtplib.SMTP(email_server)
formatter = CommitSummaryFormatter(repository_summaries);
for email_address, repository_list in user_repositories.items():
    logging.info(" - Sending summary of %d repos to %s" % (len(repository_list), email_address))
    email_body = formatter.get_formatted_summaries(repository_list)
    message = MIMEText(email_body)
    message['Subject'] = 'SVNGUT summary for %s to %s' % (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    message['From'] = email_sender
    message['To'] = email_address
    logging.info("\n%s" % email_body)
    server.sendmail(email_sender, [email_address], message.as_string())
server.quit()
logging.info("Finished SVN Gut")