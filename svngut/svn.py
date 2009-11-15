import pysvn
import time
import datetime

__all__ = ['SvnRepo', 'SvnCommit', 'SvnRepoContributor']

class Error(Exception):
    pass

class Repository(object):

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
    
    def __repr__(self):
        return "<SVN repository at %s>" % self.url

class Commit(object):
    """A commit object"""
    
    def __init__(self, revision, message, date, file_changes):
        self.revision = revision
        self.message = message.strip()
        self.date = date
        self.file_changes = file_changes
        
    def get_summary(self):
        return "[%s] %s (%s)" % (self.date.strftime("%Y-%m-%d %H:%M"), self._get_message(), self._get_file_summary())
    
    def get_num_affected_files(self):
        return len(self.file_changes)

    def get_num_new_files(self):
        return len(filter(lambda x: x.find('A: ') == 0, self.file_changes))

    def get_num_modified_files(self):
        return len(filter(lambda x: x.find('M: ') == 0, self.file_changes))

    def get_num_deleted_files(self):
        return len(filter(lambda x: x.find('D: ') == 0, self.file_changes))

    def _get_message(self):
        if self.message == "":
            return "[no message]" 
        return self.message

    def _get_file_summary(self):
        if (len(self.file_changes) == 1):
            return self.file_changes[0]
        else:
            return "%d files" % len(self.file_changes)

    def __repr__(self):
        return "<svn-commit: %d '%s' (%s)>" % (self.revision, self._get_message(), self.date.strftime("%Y-%m-%d %H:%M"))

class BranchContribution(object):
    
    def __init__(self, branch_url, commits):
        self.branch_url = branch_url
        self.commits = commits
    
    def get_num_commits(self):
        return len(self.commits)

    def get_num_affected_files(self):
        return sum(map(lambda c: c.get_num_affected_files(), self.commits))

    def get_num_new_files(self):
        return sum(map(lambda c: c.get_num_new_files(), self.commits))

    def get_num_modified_files(self):
        return sum(map(lambda c: c.get_num_modified_files(), self.commits))

    def get_num_deleted_files(self):
        return sum(map(lambda c: c.get_num_deleted_files(), self.commits))

    def get_email_summary(self):
        return "<strong>%s</strong>: %d commit(s)<br/>%s" % (self.name, len(self.commits), self._get_commits_summary())
        
    def _get_commits_summary(self):
        summaries = [commit.get_summary() for commit in self.commits] 
        return "<br/>".join(summaries)
        
    def __repr__(self):
        return "<svn-contributor: %s - %d commit(s)>" % (self.name, len(self.commits))

class UserBranchContribution(object):
    
    def __init__(self, name, contribution):
        self.name = name
        self.contribution = contribution