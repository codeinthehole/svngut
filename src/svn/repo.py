'''
Created on 17 Aug 2009

@author: david
'''
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
        commits = self._svn_client.log(repo.url, limit=20)
        return commits
