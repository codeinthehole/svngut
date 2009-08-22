from svn.repo import *
import datetime
import pysvn
import logging
import sys
import smtplib

# Set up logger
logging.basicConfig(
    stream = sys.stdout,  
    level = logging.INFO,
    format = "%(asctime)s\t%(message)s"
);
logging.info("Starting SVN gut - let the digestin' begin...")

# Import configuration
try:
    from config import svn_username, svn_password, repos, user_repos, analysis_period_in_days
except ImportError:
    logging.info("Cannot find config file (config.py)")
    sys.exit()

# Summarise configuration
logging.info("Config: found %d repo(s) to digest" % len(repos))
logging.info("Config: found %d recipient(s) to inform" % len(user_repos.keys()))

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
repo_summaries = {}
for repo in repos:
    logging.info("Checking repo: %s" % repo.url)
    try:
        commits = svn_interrogator.get_commits_for_date_range(repo, date_range)
        logging.info("Found %d commits" % len(commits))
        summary = commit_analyser.get_commit_list_summary(commits)
        for user, info in summary.items():
            logging.info(" - %s\t%d commits" % (user.ljust(20), info["commits"]))
        repo_summaries[repo] = summary
    except pysvn._pysvn.ClientError:
        logging.info("SVN client error - cannot access %s" % repo.url)
    
# Send notifications
logging.info("Sending emails...")
server = smtplib.SMTP('localhost')
formatter = CommitSummaryFormatter(repo_summaries);
for email_address, linked_repo_names in user_repos.items():
    logging.info(" - Sending summary of %d repos to %s" % (len(linked_repo_names), email_address))
    email_body = formatter.get_formatted_summaries(linked_repo_names)
    logging.info("\n%s" % email_body)
    server.sendmail('svngut@orwell.tangentlabs.co.uk', email_address, email_body)
server.quit()
logging.info("Finished SVN Gut")