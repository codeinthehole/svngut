# Repositories to analyse
# This should take the form name : url
repository_mapping = {
    'myrepo': 'http://svn.example.com/myrepo/trunk',
}

# User's linked repos - set the user's email address as the key
user_repository_mapping = {
     'user1@domain.com': ['myfirstrepo', 'mysecondrepo'],
     'user2@domain.com': ['myfirstrepo'],         
}

# SVN access credentials
svn_username = None
svn_password = None

# Misc - the number of days of SVN activity to analyse
analysis_period_in_days = 7