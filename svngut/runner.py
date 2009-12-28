# Standard library imports
import logging
import sys
import os
import smtplib

# Non-standard library imports
import pysvn

# Local imports
from svngut.configparser import Parser
from svngut.interrogator import RepositoryInterrogator
from svngut.digest import Summariser
from svngut.notify import Notifier
from svngut.svn import *


def set_up_logger():
    """Sets up the logging environment"""
    logging.basicConfig(
        stream = sys.stdout,  
        level = logging.INFO,
        format = "%(asctime)s\t%(message)s"
    );


def run(path_to_config):
    
    set_up_logger()
    logging.info("==============================")
    logging.info("SVNGUT - by David Winterbottom")
    logging.info("==============================")
    
    # Read configuration
    parser = Parser(path_to_config)
    date_range = parser.get_date_range()
    logging.info("Analysis period between %s and %s", date_range[0], date_range[1])
    repositories = parser.get_repositories() 
    logging.info("Found %d repositories to analyse..." % len(repositories))
    
    # Fetch branch contributions for each repository
    all_branch_contributions = {}
    interrogator = RepositoryInterrogator(pysvn.Client())
    for repository_key, repository in repositories.items():
        all_branch_contributions[repository_key] = interrogator.get_all_branch_contributions(repository, date_range)
    
    # Generate summary HTML
    path_to_template = os.path.join(os.path.dirname(__file__), 'templates/summary.html')
    digestor = Summariser(path_to_template, all_branch_contributions)
    summary_html = digestor.get_summary_html()
    
    # Send notifications
    server = smtplib.SMTP('localhost', 'svngut@orwell.tangentlabs.co.uk')
    notifier = Notifier(server)
    notifier.send_emails('david.winterbottom@gmail.com', summary_html)
    
if __name__ == '__main__':
    run()      