from lookup import *
from runtime import *
import datetime
import pysvn
import logging
import sys
from mako.template import Template
import smtplib
from email.mime.text import MIMEText
from pprint import pprint as d

def run():

# Set up logger
    logging.basicConfig(
        stream = sys.stdout,  
        level = logging.INFO,
        format = "%(asctime)s\t%(message)s"
    );
    logging.info("SVNGUT - by David Winterbottom")

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

    d(repositories)

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
        contributions = interrogator.get_contributions(repo, date_range)
        repository_contributions[repo.url] = contributions

# Summary stats for all repos
    contributor_stats = {}
    for repo, contributions in repository_contributions.items():
        for contribution in contributions:
            name = contribution.name
            if contributor_stats.has_key(name):
                contributor_stats[name]['commits'] += contribution.get_num_commits()
                contributor_stats[name]['affected_files'] += contribution.get_num_affected_files()
                contributor_stats[name]['new_files'] += contribution.get_num_new_files()
                contributor_stats[name]['modified_files'] += contribution.get_num_modified_files()
            else:
                contributor_stats[name] = {
                    'name': name,
                    'commits': contribution.get_num_commits(),
                    'affected_files': contribution.get_num_affected_files(),
                    'new_files': contribution.get_num_new_files(),
                    'modified_files': contribution.get_num_modified_files(),
                }

# Send notifications
    logging.info("Sending notification emails...")
    server = smtplib.SMTP(email_server)
    for email_address, repository_list in user_repositories.items():
        logging.info(" - Sending summary of %d repo(s) to %s" % (len(repository_list), email_address))

        # Construct email body (need to refactor to use templating language)
        #email_template = Template(filename='templates/summary.html')
        #email_body = email_template.render(contributor_stats=contributor_stats)
        #print email_body
        #sys.exit()

        email_body = "<html>"
        email_body += "<h1>Overall statistics</h1>"
        email_body += "<table><tr><th>Name</th><th>Commits</th><th>Num files</th></tr>"
        for contributor in contributor_stats.values():
            email_body += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % \
                    (contributor['name'], contributor['commits'], contributor['affected_files'])
        email_body += "</table>"

        email_body += "<h1>Breakdown</h1>"
        for repo in repository_list:
            contributions = repository_contributions[repo.url]
            if (len(contributions) > 0): 
                email_body += "Repository: <strong>%s</strong>" % repo.url
                email_body += "<ol><li>"
                email_body += "</li><li>".join([contribution.get_email_summary() for contribution in contributions])
                email_body += "</li></ol>"
        email_body += "</html>"

        f = open('/tmp/svngut-email.html', 'w')
        f.write(email_body)
        f.close()

        message = MIMEText(email_body, 'html')
        message['Subject'] = 'SVNGUT summary for %s' % (start_date.strftime("%Y-%m-%d"))
        message['From'] = email_sender
        message['To'] = email_address
        server.sendmail(email_sender, [email_address], message.as_string())
    server.quit()
    logging.info("Finished SVN Gut")   