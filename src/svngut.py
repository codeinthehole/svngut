"""Analyse SVN repositories for sending summary emails

Classes:

	Repo
	CommitRetriever
	CommitSummariser
	CommitSummaryFormatter

"""

import pysvn
import time
import datetime

__all__ = ['SvnRepo', 'SvnRepoContributor', 'SvnCommitRetriever']

class SvngutError(Exception):
    pass

class SvnRepo(object):

    def __init__(self, url, user, password):
        """This takes the SVN location and credentials"""
        self.url = url
        self.user = user
        self.password = password
    
    def __repr__(self):
        return "<SVN repository at %s>" % self.url
    
class SvnCommit(object):
    
    def __init__(self, revision, message, date, file_changes):
        self.revision = revision
        self.message = message.strip()
        self.date = date
        self.file_changes = file_changes
        
    def __repr__(self):
        return "<svn-commit: %d '%s' (%s)>" % (self.revision, self._get_message(), self.date.strftime("%Y-%m-%d %H:%M"))

    def get_summary(self):
        return "[%s] %s (%s)" % (self.date.strftime("%Y-%m-%d %H:%M"), self._get_message(), self._get_file_summary())
    
    def _get_message(self):
        if self.message == "":
            return "<no message>" 
        return self.message

    def _get_file_summary(self):
        if (len(self.file_changes) == 1):
            return self.file_changes[0]
        else:
            return "%d files" % len(self.file_changes)


class SvnRepoContributor(object):
    
    def __init__(self, name, commits):
        self.name = name
        self.commits = commits
    
    def get_email_summary(self):
        return "%s: %d commit(s)<br/>%s" % (self.name, len(self.commits), self._get_commits_summary())
        
    def _get_commits_summary(self):
        summaries = [commit.get_summary() for commit in self.commits] 
        return "<br/>".join(summaries)
        
    def __repr__(self):
        return "<svn-contributor: %s - %d commit(s)>" % (self.name, len(self.commits))

class SvnCommitRetriever(object):
    
    def __init__(self, svn_client):
        self._svn_client = svn_client
    
    def get_contributors(self, repo, date_range):
        raw_commits = self._get_raw_commits(repo, date_range)
        raw_commits_by_user = self._get_raw_user_commit_lists(raw_commits)
        processed_commits_by_user = self._get_processed_user_commit_lists(raw_commits_by_user)
        return [SvnRepoContributor(name, commits) for name, commits in processed_commits_by_user.items()]
    
    def _get_raw_commits(self, repo, date_range):
        start_revision = pysvn.Revision(pysvn.opt_revision_kind.date, time.mktime(date_range[0].timetuple()))
        end_revision = pysvn.Revision(pysvn.opt_revision_kind.date, time.mktime(date_range[1].timetuple()))
        raw_commits = self._svn_client.log(repo.url, 
                                    revision_start=start_revision, 
                                    revision_end=end_revision,
                                    discover_changed_paths=True)
        # Need to double-check dates as the revision look-up method isn't 100% watertight
        start_timestamp = date_range[0].time()
        filtered_commits = []
        for commit in raw_commits:
            commit_datetime = datetime.datetime.fromtimestamp(commit.date)
            if commit_datetime > date_range[0] and commit_datetime < date_range[1]:
                filtered_commits.append(commit)
        return filtered_commits

    def _get_raw_user_commit_lists(self, all_commits):
        user_commits = {}
        for commit in all_commits:
            if commit.author not in user_commits:
                user_commits[commit.author] = [commit]
            else:
                user_commits[commit.author].append(commit)
        return user_commits
        
    def _get_processed_user_commit_lists(self, user_commit_lists):
        user_commits = {}
        for author, raw_commits in user_commit_lists.items():
            user_commits[author] = self._get_processed_commits(raw_commits)
        return user_commits
    
    def _get_processed_commits(self, raw_commits):
        return [self._get_processed_commit(raw_commit) for raw_commit in raw_commits]
    
    def _get_processed_commit(self, raw_commit):
        return SvnCommit(raw_commit.revision.number, 
                raw_commit.message, 
                datetime.datetime.fromtimestamp(raw_commit.date), 
                self._get_commit_file_changes(raw_commit))
    
    def _get_commit_file_changes(self, raw_commit):
        lines = []
        for path_change in raw_commit.changed_paths:
            lines.append("%s: %s" % (path_change['action'], path_change['path']))
        return lines
