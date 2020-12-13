from string import ascii_uppercase
import random


def get(number_of_projects, key_length=2, sort_asc=False, projects=None):
    """Return a list of projects"""
    if not isinstance(projects, list):
        projects = []

    project_keys = _generate_keys(number_of_projects, key_length, sort_asc)

    for key in project_keys:
        projects.append({
            'projectKey': key,
            'projectName': f'{key} project',
            'projectDescription': None,
        })
    return projects


def _generate_keys(number_of_projects, key_length=2, sort_asc=False, project_keys=None):
    """Generate a list of unique project keys"""
    if not isinstance(project_keys, set):
        project_keys = set()

    while len(project_keys) < number_of_projects:
        project_keys.add(_get_key(key_length))
    project_keys = list(project_keys)

    if sort_asc:
        project_keys.sort()

    return project_keys[:]


def _get_key(length=2):
    """Generate a project key"""
    letters = ascii_uppercase
    project_key = ''.join([random.choice(letters) for i in range(0, length)])
    return project_key
