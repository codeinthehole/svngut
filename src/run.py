from svn.repo import Repo, CommitRetriever
import datetime
import pysvn

# Create collection of repositories
(user, password) = "taobase-deployment", "unit105"
repo_urls = ["http://dev.tangentlabs.co.uk/svn/%s/trunk" % name for name in ['taoshop']]      
repos = [Repo(url, user, password) for url in repo_urls]

# Get date range for analysis
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=30)
date_range = (start_date, end_date)

# Analyse commits
svn_interrogator = CommitRetriever(pysvn.Client())
for repo in repos:
    commits = svn_interrogator.get_commits_for_date_range(repo, date_range)
    commit_info = {}
    for commit in commits:
        if commit.author not in commit_info:
            commit_info[commit.author] = {"name": commit.author, "commits": 1}
        else:
            commit_info[commit.author]["commits"] += 1
    print commit_info    