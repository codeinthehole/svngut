from svn.repo import *
import datetime
import pysvn
import logging
import sys
import smtplib

# Import configuration
from config import svn_username, svn_password, repos, user_repos, analysis_period_in_days

# Set up logger
logging.basicConfig(
    stream = sys.stdout,  
    level = logging.INFO,
    format = "%(asctime)s\t%(message)s"
);
logging.info("Starting SVN gut - let the digestin' begin...")

# Summarise configuration
logging.info("Config: found %d repos to digest" % len(repos))
logging.info("Config: found %d recipients to inform" % len(user_repos.keys()))

# Get date range for analysis
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=analysis_period_in_days)
date_range = (start_date, end_date)
logging.info("Date range: %s to %s (last %d days)" % \
             (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), analysis_period_in_days))

# Analyse commits
repos = [Repo(url, svn_username, svn_password) for url in repos.values()]
svn_interrogator = CommitRetriever(pysvn.Client())
commit_analyser = CommitSummariser()
for repo in repos:
    logging.info("Checking repo: %s" % repo.url)
    commits = svn_interrogator.get_commits_for_date_range(repo, date_range)
    logging.info("Found %d commits" % len(commits))
    summary = commit_analyser.get_commit_list_summary(commits)
    for user, info in summary.items():
        logging.info(" - %s\t%d commits" % (user.ljust(20), info["commits"]))
    
# Format commit summary
formatter = Formatter()

# Send notifications
logging.info("Sending emails...")
server = smtplib.SMTP('localhost')
for email_address, linked_repo_names in user_repos:
    logging.info(" - Sending summary to %s" % email_address)
    email_body = ", ".join(linked_repo_names)
    server.sendmail('svngut@orwell.tangentlabs.co.uk', email_address, email_body)
server.quit()