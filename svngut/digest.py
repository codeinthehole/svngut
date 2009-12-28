from mako.template import Template

class Summariser(object):
    """Service object responsible for converting a set of repository branch
       contributions into a HTML summary"""
    
    def __init__(self, path_to_template_file, repository_branch_contributions):
        self.path_to_template_file = path_to_template_file
        self.repository_branch_contributions = repository_branch_contributions
    
    def get_summary_html(self):
        """Returns summary HTML for the repository branch contributions"""
        template = Template(filename=self.path_to_template_file)
        return template.render(user_stats=self._get_user_stats(),
                               branch_stats=self._get_branch_stats(),
                               repo_branch_contributions=self.repository_branch_contributions)

    def _get_user_stats(self):
        """Returns a dict of stats broken down by user"""
        stats = {}
        for branch_contributions in self.repository_branch_contributions.values():
            for contributions in branch_contributions.values():
                for username, contribution in contributions.items():
                    if not stats.has_key(username):
                        stats[username] = {'name': username, \
                                           'repository_contributions': 0,
                                           'num_commits': 0,
                                           'num_added_files': 0,
                                           'num_modified_files': 0,
                                           'num_deleted_files': 0}
                    stats[username]['repository_contributions'] += 1
                    stats[username]['num_commits'] += contribution.get_num_commits()
                    stats[username]['num_added_files'] += contribution.get_num_new_files()
                    stats[username]['num_modified_files'] += contribution.get_num_modified_files()
                    stats[username]['num_deleted_files'] += contribution.get_num_deleted_files()
        return stats                                

    def _get_branch_stats(self):
        """Returns a dict of stats broken down by branch"""
        stats = {}
        for branch_contributions in self.repository_branch_contributions.values():
            for branch_url, contributions in branch_contributions.items():
                if not stats.has_key(branch_url):
                    stats[branch_url] = {'name': branch_url,
                                        'repository_contributions': 0,
                                        'num_commits': 0,
                                        'num_added_files': 0,
                                        'num_modified_files': 0,
                                        'num_deleted_files': 0}
                for contribution in contributions.values():
                    stats[branch_url]['repository_contributions'] += 1
                    stats[branch_url]['num_commits'] += contribution.get_num_commits()
                    stats[branch_url]['num_added_files'] += contribution.get_num_new_files()
                    stats[branch_url]['num_modified_files'] += contribution.get_num_modified_files()
                    stats[branch_url]['num_deleted_files'] += contribution.get_num_deleted_files()
        return stats                                