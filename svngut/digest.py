from mako.template import Template

class Summariser(object):
    
    def __init__(self, path_to_template_file):
        self.path_to_template_file = path_to_template_file
    
    def get_summary_html(self, repository_branch_contributions):
        self.repository_branch_contributions = repository_branch_contributions
        template = Template(filename=self.path_to_template_file)
        user_stats = self._get_user_stats()
        print user_stats
        return template.render(user_stats=user_stats)

    def _get_user_stats(self):
        stats = {}
        for repo_key, branch_contributions in self.repository_branch_contributions.items():
            for branch_url, contributions in branch_contributions.items():
                for username, contribution in contributions.items():
                    if not stats.has_key(username):
                        stats[username] = {'username': username, \
                                           'repository_contributions': 1,
                                           'num_commits': len(contribution.commits)}
                    else:
                        stats[username]['repository_contributions'] += 1
                        stats[username]['num_commits'] += len(contribution.commits)
        return stats                                


def old_run():    
    
    # Summary stats for all repos
    contributor_stats = {}
    for repo, contributions in repository_contributions.items():
        for contribution in contributions:
            name = contribution.name
            if contributor_stats.has_key(name):
                contributor_stats[name]['commits'] += contribution.get_num_commits()
                contributor_stats[name]['affected_files'] += contribution.get_num_affected_files()
                contributor_stats[name]['new_files'] += contribution.get_num_new_files()
                contributor_stats[name]['modified_files'] += contribution.get_num_modified_files()
            else:
                contributor_stats[name] = {
                    'name': name,
                    'commits': contribution.get_num_commits(),
                    'affected_files': contribution.get_num_affected_files(),
                    'new_files': contribution.get_num_new_files(),
                    'modified_files': contribution.get_num_modified_files(),
                }

    # Send notifications
    logging.info("Sending notification emails...")
    server = smtplib.SMTP(email_server)
    for email_address, repository_list in user_repositories.items():
        logging.info(" - Sending summary of %d repo(s) to %s" % (len(repository_list), email_address))

        # Construct email body (need to refactor to use templating language)
        #email_template = Template(filename='templates/summary.html')
        #email_body = email_template.render(contributor_stats=contributor_stats)
        #print email_body
        #sys.exit()

        email_body = "<html>"
        email_body += "<h1>Overall statistics</h1>"
        email_body += "<table><tr><th>Name</th><th>Commits</th><th>Num files</th></tr>"
        for contributor in contributor_stats.values():
            email_body += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % \
                    (contributor['name'], contributor['commits'], contributor['affected_files'])
        email_body += "</table>"

        email_body += "<h1>Breakdown</h1>"
        for repo in repository_list:
            contributions = repository_contributions[repo.url]
            if (len(contributions) > 0): 
                email_body += "Repository: <strong>%s</strong>" % repo.url
                email_body += "<ol><li>"
                email_body += "</li><li>".join([contribution.get_email_summary() for contribution in contributions])
                email_body += "</li></ol>"
        email_body += "</html>"

        f = open('/tmp/svngut-email.html', 'w')
        f.write(email_body)
        f.close()

        message = MIMEText(email_body, 'html')
        message['Subject'] = 'SVNGUT summary for %s' % (start_date.strftime("%Y-%m-%d"))
        message['From'] = email_sender
        message['To'] = email_address
        server.sendmail(email_sender, [email_address], message.as_string())
    server.quit()
    logging.info("Finished SVN Gut")  