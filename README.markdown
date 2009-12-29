SVNGUT
======

This is a simple python utility for digesting SVN repositories and sending a periodic
summary email to a configurable list of recipients.  

Configuration
=============
To configure your local install, copy the /etc/config-sample.json to /etc/config.json
and update the listings.

Testing
=======
To run the unit tests and generate coverage statistics and reports, use the wrapper script:
> tests/unit/run_tests.sh
