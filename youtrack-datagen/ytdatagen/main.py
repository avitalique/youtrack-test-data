import argparse
import sys

from ytdatagen import config, comment, issue, project, user, writer


def entry():
    """Entry point: get CLI args and run main()"""
    p, u, i = get_cli_args()
    if config.DEBUG_MODE:
        main()
    else:
        main(p, u, i)


def main(total_projects=1, total_users=1, total_issues=10):
    """Do main work"""
    print(f'Generating test data: projects={total_projects}, users={total_users}, issues={total_issues}')

    projects = project.get(total_projects, key_length=config.PROJECT_KEY_LENGTH, sort_asc=True)
    project_keys = [p.get('projectKey') for p in projects]

    users = user.get(total_users, project_keys)
    users_by_project = user.by_project(users, project_keys)

    issue_count_by_project = issue.count_by_project(project_keys, total_issues)
    issues = issue.get(projects, users_by_project, issue_count_by_project)

    comments = comment.get(issues, users_by_project)
    issues_with_comments = comment.bind2issues(issues, comments)

    if config.IS_JMETER:
        print('Saving data as JSON strings to .csv file')
        for alias, dataset in {
            'projects': projects,
            'users': users,
            'issues': issues_with_comments,
        }.items():
            writer.json_objects_to_str(dataset, f'{alias}_json-strings.csv')

    if config.IS_CSV_IMPORT:    # is not implemented yet
        for alias, dataset in {
            'projects': projects,
            'users': users,
            'issues': issues,
            'comments': comments,
        }.items():
            # writer.to_csv(dataset, f'{alias}.csv')
            # writer.to_json(dataset, f'{alias}.json')
            pass

    if config.DEBUG_MODE:
        print(f'projects={projects}')
        print(f'project_keys={project_keys}')
        print(f'users={users}')
        print(f'users_by_project={users_by_project}')
        print(f'issue_count_by_project={issue_count_by_project}')
        # print(f'issues={issues}')
        # print(f'issues={issues_with_comments}')


def get_cli_args():
    """Parse CLI arguments"""
    parser = argparse.ArgumentParser(
        prog='yt-test-data',
        description='Test data generator for YouTrack',
    )
    parser.add_argument('-p', type=int, dest='projects_num', help='number of projects')
    parser.add_argument('-u', type=int, dest='users_num', help='number of users')
    parser.add_argument('-i', type=int, dest='issues_num', help='number of issues')
    parser.add_argument('-d', dest='is_default', action='store_true',
                        help='generate default volume of data (projects = 10, users = 100, issues = 50000)')
    parser.add_argument('--jmeter', dest='is_jmeter', action='store_true',
                        help='Save data to CSV files as JSON strings')
    parser.add_argument('--csv-import', dest='is_csv_import', action='store_true',
                        help='Save data to CSV files according to YouTrack import scripts requirements')
    parser.add_argument('--debug', dest='debug_mode', action='store_true',
                        help='Run in debug mode. Generated data will not be saved to files, but printed to stdout')

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    projects_num = args.projects_num
    users_num = args.users_num
    issues_num = args.issues_num

    if args.is_default:
        projects_num = 10
        users_num = 100
        issues_num = 50000
    elif not args.projects_num or not args.users_num or not args.issues_num:
        parser.print_usage()
        missing = []
        if not args.projects_num:
            missing.append('-p')
        if not args.users_num:
            missing.append('-u')
        if not args.issues_num:
            missing.append('-i')
        parser.exit(2, f'{parser.prog}: error: missing arguments: {", ".join(missing)}')

    config.DEBUG_MODE = args.debug_mode
    config.IS_JMETER = args.is_jmeter
    config.IS_CSV_IMPORT = args.is_csv_import

    if not config.IS_CSV_IMPORT:  # and not config.DEBUG_MODE:
        config.IS_JMETER = True

    return projects_num, users_num, issues_num


if __name__ == '__main__':
    entry()
