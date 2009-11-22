import re
import datetime
import time
import pysvn

from svngut.svn import *

class RepositoryInterrogator(object):
    
    def __init__(self, svn_client):
        self.client = svn_client

    def get_branch_contributions(self, repository, date_range):
        for branch_url in self.get_branch_urls(repository):
            pass
        
    def get_branch_urls(self, repository):
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

    def _get_processed_commits(self, raw_commits):
        return [self._get_processed_commit(raw_commit) for raw_commit in raw_commits]
        
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
