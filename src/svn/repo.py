import pysvn
import time

__all__ = ['Repo', 'CommitRetriever', 'CommitSummariser', 'CommitSummaryFormatter']

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
    
class CommitSummariser(object):
    def get_commit_list_summary(self, commit_list): 
        commit_summary = {}
        for commit in commit_list:
            if commit.author not in commit_summary:
                commit_summary[commit.author] = {"name": commit.author, "commits": 1}
            else:
                commit_summary[commit.author]["commits"] += 1
        return commit_summary

class CommitSummaryFormatter(object):
    def __init__(self, repo_summaries):
        self.summaries = repo_summaries
    
    def get_formatted_summaries(self, repo_list):
        formatted_summaries = []
        for repo in repo_list:
            formatted_summaries.append(self.get_formatted_repo(repo))
        return "\n".join(formatted_summaries) 
    
    def get_formatted_repo(self, repo):
        return repo