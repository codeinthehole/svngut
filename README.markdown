# SVNGUT

This is a simple python utility for digesting SVN repositories and sending a periodic
summary email to a configurable list of recipients.  It uses a JSON configuration file 
to specify the repositories to digest and also which users should get a summary email.  
Each user can receive a digest of a different set of repositories if so desired.

This utility is intended to be useful for team/project leaders, who want to stay in 
touch with all SVN activity of the projects they are interested in.

All comments, criticism, bugs to david.winterbottom@gmail.com please.

## Installation
* clone repository
* Add svngut to your PYTHON_PATH:
    ln -s /path/to/clone /usr/lib/python2.6/dist-packages/svngut

## Configuration
To configure your local install, copy the /etc/config-sample.json to /etc/config.json
and update the listings.

## Testing
To run the unit tests and generate coverage statistics and reports, use the wrapper script:
    tests/unit/run_tests.sh
