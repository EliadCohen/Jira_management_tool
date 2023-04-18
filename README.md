# Jira management tools

## How to use create_stories.py

Creating stories for Dev, QE and Docs for a given Epic

### Install dependencies

$ pip install -r requirements.txt

### Create an auth.cfg file, for an example:

'''
[jira]
jira_server = <url>
project = <project name>
[auth]
token = <token>
'''

### Run create_stories.py for the creation of all of the stories for an epic

'''
$ create_stories.py --auth-file auth.cfg --epic-id <Epic name> \
 --design true \
 --implementation true \
 --test-case true \
 --automate true \
 --ci-automation true \
 --documentation true \
 --dev-assignee <username> \
 --qe-assignee <username> \
 --workstream <workstream>
'''
