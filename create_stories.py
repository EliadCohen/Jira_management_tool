import argparse
from jira import JIRA
import configparser


def create_stories(jira, epic, test_case=None, automate=None, ci_automation=None):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth-file')
    parser.add_argument('--epic-id')
    parser.add_argument('--design', default=None)
    parser.add_argument('--implementation', default=None)
    parser.add_argument('--test-case', default=None)
    parser.add_argument('--automate', default=None)
    parser.add_argument('--ci-automation', default=None)
    parser.add_argument('--documentation', default=None)
    parser.add_argument('--dev-assignee', default=None)
    parser.add_argument('--qe-assignee', default=None)
    parser.add_argument('--doc-assignee', default=None)
    parser.add_argument('--workstream', default=None)

    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.auth_file)

    token = config['auth']['token']
    options = {
        'server': config['jira']['jira_server']
    }

    jira = JIRA(options, token_auth=token)
    epic = jira.issue(args.epic_id)
    fix_versions = epic.fields.fixVersions[0]

    if args.design:
        design = jira.create_issue(fields={
            'project': config['jira']['project'],
            'issuetype': 'Story',
            'customfield_12311140': epic.key,
            'summary': '[Dev]Write design doc for %s' % epic.key,
            'description': 'Write design doc for %s.' % epic.key,
        })
        design.update(fields={'fixVersions': [{'name': fix_versions.name}]})
        if args.dev_assignee:
            design.update(assignee=args.dev_assignee)
        if args.workstream:
            design.update(
                fields={'customfield_12319275': [{"value": args.workstream}]})
        print('Design story: %s created successfully' % design.key)

    if args.implementation:
        implementation = jira.create_issue(fields={
            'project': config['jira']['project'],
            'issuetype': 'Story',
            'customfield_12311140': epic.key,
            'summary': '[Dev]Implement %s' % epic.key,
            'description': 'Implement %s.' % epic.key,
        })
        implementation.update(
            fields={'fixVersions': [{'name': fix_versions.name}]})
        if args.dev_assignee:
            implementation.update(assignee=args.dev_assignee)
        if args.workstream:
            implementation.update(
                fields={'customfield_12319275': [{"value": args.workstream}]})
        print('Implementation story: %s created successfully' %
              implementation.key)

    if args.test_case:
        test_case = jira.create_issue(fields={
            'project': config['jira']['project'],
            'issuetype': 'Story',
            'customfield_12311140': epic.key,
            'summary': '[QE]Create test cases for %s' % epic.key,
            'description': 'Create  test cases for %s.' % epic.key,
        })
        test_case.update(fields={'fixVersions': [{'name': fix_versions.name}]})
        if args.qe_assignee:
            test_case.update(assignee=args.qe_assignee)
        if args.workstream:
            test_case.update(
                fields={'customfield_12319275': [{"value": args.workstream}]})
        print('Test case story: %s created successfully' % test_case.key)

    if args.automate:
        automate = jira.create_issue(fields={
            'project': config['jira']['project'],
            'issuetype': 'Story',
            'customfield_12311140': epic.key,
            'summary': '[QE]Automate funcional tests for %s' % epic.key,
            'description': 'Automate funcional tests for %s.' % epic.key
        })
        automate.update(fields={'fixVersions': [{'name': fix_versions.name}]})
        if args.qe_assignee:
            automate.update(assignee=args.qe_assignee)
        if args.workstream:
            automate.update(fields={'customfield_12319275': [
                            {"value": args.workstream}]})
        print('Automate functional tests story: %s created successfully' %
              automate.key)

    if args.ci_automation:
        ci_automation = jira.create_issue(fields={
            'project': config['jira']['project'],
            'issuetype': 'Story',
            'customfield_12311140': epic.key,
            'summary': '[QE]Enable funcional tests for %s in CI' % epic.key,
            'description': 'Enable funcional tests for %s in CI' % epic.key
        })
        ci_automation.update(
            fields={'fixVersions': [{'name': fix_versions.name}]})
        if args.qe_assignee:
            ci_automation.update(assignee=args.qe_assignee)
        if args.workstream:
            ci_automation.update(fields={'customfield_12319275': [
                                 {"value": args.workstream}]})
        print('CI automation enablement story: %s created successfully' %
              ci_automation.key)

        if args.documentaiton:
            documentation = jira.create_issue(fields={
                'project': config['jira']['project'],
                'issuetype': 'Story',
                'customfield_12311140': epic.key,
                'summary': '[Docs] Document %s' % epic.key,
                'description': 'Document %s' % epic.key
            })
        documentation.update(
            fields={'fixVersions': [{'name': fix_versions.name}]})
        if args.doc_assignee:
            documentation.update(assignee=args.doc_assignee)
        if args.workstream:
            documentation.update(fields={'customfield_12319275': [
                                 {"value": args.workstream}]})
        print('Docmentation story: %s created successfully' %
              documentation.key)


# whiteboard == customfield_12316843
# parent link == custmfield_12311140
# workstream == customfield_12319275


if __name__ == '__main__':
    main()
