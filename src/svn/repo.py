import pysvn
import time

class Repo(object):
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
    def __repr__(self):
        return "<SVN repository at %s>" % self.url
    
class CommitRetriever(object):
    def __init__(self, svn_client):
        self._svn_client = svn_client
    def get_commits_for_date_range(self, repo, date_range):
        start_revision = pysvn.Revision(pysvn.opt_revision_kind.date, time.mktime(date_range[0].timetuple()))
        end_revision = pysvn.Revision(pysvn.opt_revision_kind.date, time.mktime(date_range[1].timetuple()))
        
        commits = self._svn_client.log(repo.url, revision_start=start_revision, revision_end=end_revision)
        return commits
