import re
import datetime
import time
import pysvn
import logging

from svngut.svn import *

class RepositoryInterrogator(object):
    
    def __init__(self, svn_client):
        self.client = svn_client

    def get_all_branch_contributions(self, repository, date_range):
        """Returns the branch contributions for a given repository"""
        contributions = {}
        logging.info("Analysing %s", repository.url)
        for branch_url in self.get_branch_urls(repository):
            logging.info("Fetching commits on branch: %s", branch_url)
            contributions[branch_url] = self.get_branch_contributions(branch_url, date_range)
        return contributions
        
    def get_branch_urls(self, repository):
        """Returns a list of the branch URLs that require analysing"""
        base_urls = self.get_url_list(repository.url)
        branch_urls = []
        for url in base_urls:
            if re.search('/trunk/?', url) != None:
                branch_urls.append(url)
            if re.search('/branches/?', url) != None:
                branch_urls += self.get_url_list(url)
        return branch_urls

    def get_url_list(self, url):
        urls = []
        for svn_dir in self.client.ls(url):
            urls.append(svn_dir['name'])
        return urls
    
    def get_branch_contributions(self, url, date_range):
        """Returns a dict of user branch contributions."""
        
        # Retrive all commits for the date range
        raw_commits = self._get_raw_commits_by_url(url, date_range)
        
        # Split by username into separate lists of converted commits
        user_contributions = {}
        for raw_commit in raw_commits:
            username = raw_commit.author
            commit = self._get_processed_commit(raw_commit)
            if user_contributions.has_key(username):
                user_contributions[username].append(commit)
            else:
                user_contributions[username] = [commit]
        
        # Create branch contributions objects
        user_branch_contributions= {}
        for username, commits in user_contributions.items():
            user_branch_contributions[username] = BranchContribution(username, url, commits)
        
        return user_branch_contributions
    
    def get_commits_by_url(self, url, date_range):
        raw_commits = self._get_raw_commits_by_url(url, date_range)
        
        return self._get_processed_commits(raw_commits)
    
    def _get_raw_commits_by_url(self, url, date_range):
        start_revision = pysvn.Revision(pysvn.opt_revision_kind.date, 
                                        time.mktime(date_range[0].timetuple()))
        end_revision = pysvn.Revision(pysvn.opt_revision_kind.date, 
                                      time.mktime(date_range[1].timetuple()))
        raw_commits = self.client.log(url, 
                                      revision_start=start_revision, 
                                      revision_end=end_revision,
                                      discover_changed_paths=True)
        
        # Need to double-check dates as the revision look-up method isn't 100% watertight
        filtered_raw_commits = []
        for commit in raw_commits:
            commit_datetime = datetime.datetime.fromtimestamp(commit.date)
            if commit_datetime > date_range[0] and commit_datetime < date_range[1]:
                filtered_raw_commits.append(commit)
        return filtered_raw_commits
        
    def _get_processed_commit(self, raw_commit):
        return Commit(raw_commit.revision.number, 
                      raw_commit.message, 
                      datetime.datetime.fromtimestamp(raw_commit.date), 
                      self._get_commit_file_changes(raw_commit))    

    def _get_commit_file_changes(self, raw_commit):
        lines = []
        for path_change in raw_commit.changed_paths:
            lines.append("%s: %s" % (path_change['action'], path_change['path']))
        return lines
