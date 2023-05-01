import argparse
from jira import JIRA
import jira
import configparser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth-file')
    parser.add_argument('--update-issues')
    parser.add_argument('--update-children')
    parser.add_argument('--issue-id', nargs='*', default=None)
    parser.add_argument('--set-components', nargs='*', default=None)
    parser.add_argument('--fix-versions', nargs='*', default=None)
    parser.add_argument('--affected-versions', nargs='*', default=None)
    parser.add_argument('--set-labels', nargs='*', default=None)
    parser.add_argument('--set-type')
    parser.add_argument('--set-status')
    parser.add_argument('--set-priority')
    parser.add_argument(
        '--is-blocked', choices=['false', 'true', 'none', 'True', 'False', 'None'])
    parser.add_argument(
        '--is-ready', choices=['false', 'true', 'none', 'True', 'False', 'None'])
    parser.add_argument('--set-workstreams', nargs='*', default=None)
    parser.add_argument('--set-epic-link')
    parser.add_argument('--blocks-issues', nargs='*', default=None)
    parser.add_argument('--blocked-by-issues', nargs='*', default=None)
    parser.add_argument('--comment')

    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.auth_file)

    token = config['auth']['token']
    options = {
        'server': config['jira']['jira_server']
    }

    fixed_versions = []
    components = []
    affected_versions = []
    labels = []
    workstreams = []
    update_fields = {}
    jira = JIRA(options, token_auth=token)

    if args.update_issues:
        for issue in args.issue_id:
            tmp = jira.issue(issue)

            if args.comment:
                jira.add_comment(tmp.id, args.comment)

            if args.blocked_by_issues:
                for blocking_issue in args.blocked_by_issues:
                    jira.create_issue_link(
                        inwardIssue=blocker_issue, outwardIssue=tmp.key, type='blocks')

            if args.blocks_issues:
                # outwardIssue == the blocking issue
                for blocker_issue in args.blocks_issues:
                    jira.create_issue_link(
                        inwardIssue=tmp.key, outwardIssue=blocker_issue, type='blocks')

            if args.set_workstreams:
                for workstream in args.set_workstreams:
                    workstreams.append({'value': workstream})
                update_fields['customfield_12319275'] = workstreams

            if args.is_ready:
                update_fields['customfield_12316542'] = {
                    'value': args.is_ready.capitalize()}

            if args.is_blocked:
                update_fields['customfield_12316543'] = {
                    'value': args.is_blocked.capitalize()}

            if args.set_priority:
                update_fields['priority'] = {'name': args.set_priority}

            # update status -> jira.transition_issue()
            if args.set_status:
                jira.transition_issue(tmp.id, args.set_status)

            if args.set_type:
                update_fields['issuetype'] = {"name": args.set_type}

            if args.set_labels:
                for label in args.set_labels:
                    labels.append(label)
                update_fields['labels'] = labels

            if args.fix_versions:
                for version in args.fix_versions:
                    fixed_versions.append({'name': version})
                update_fields['fixVersions'] = fixed_versions

            if args.affected_versions:
                for version in args.affected_versions:
                    affected_versions.append({'name': version})
                update_fields['versions'] = affected_versions

            if args.set_components:
                for component in args.set_components:
                    components.append({'add': {'name': component}})
                tmp.update(update={'components': components})

            print(update_fields)
            tmp.update(fields=update_fields)


if __name__ == '__main__':
    main()
