import simplejson
import os.path
import datetime
from svngut.svn import Repository

class Parser(object):

    def __init__(self, path_to_config_file):
        if not os.path.isfile(path_to_config_file):
            raise OSError("Could not find file %s" % path_to_config_file)
        self.json = simplejson.load(open(path_to_config_file))
        
    def get_repositories(self):
        repositories = {}
        for repo_key in self.json['repositories']:
            repository = Repository(self.json['repositories'][repo_key]['url'])
            username = self.json['repositories'][repo_key]['username']
            password = self.json['repositories'][repo_key]['password']
            repository.set_credentials(username, password)
            repositories[repo_key] = repository
        return repositories
    
    def get_date_range(self):
        today = datetime.date.today()
        start_date = datetime.datetime(today.year, today.month, today.day-self.get_analysis_period(), 0, 0, 0)
        end_date = datetime.datetime(today.year, today.month, today.day-1, 23, 59, 59)
        return (start_date, end_date)
    
    def get_analysis_period(self):
        return self.json['analysis_period_in_days']
        