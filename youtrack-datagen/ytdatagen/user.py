import random
import requests


def get(total_users, project_keys=None):
    """Return list of users"""
    users = []
    if not isinstance(project_keys, list):
        project_keys = []

    user_names = _get_names(total_users)

    for name in user_names:
        users.append({
            'userName': name,
            'userLogin': _get_login(name),
            'userEmail': _get_email(name),
            'projectKey': _get_project_key(project_keys),
        })

    return users


def by_project(users, project_keys):
    """Return a map of user names by project"""
    project_users = {}
    for k in project_keys:
        project_users[k] = [u['userName'] for u in users if u['projectKey'] == k]
    return project_users


def _get_names(number_of_names):
    """Get list of random names from API: http://names.drycodes.com/"""
    number_of_males = int(number_of_names / 100 * random.randint(40, 60))
    number_of_females = number_of_names - number_of_males

    names = []
    for gender, count in {'boy': number_of_males, 'girl': number_of_females}.items():
        r = requests.get(
            f'http://names.drycodes.com/{count}?nameOptions={gender}_names&separator=space'
        )
        names += r.json()
    random.shuffle(names)

    return [names[i] for i in range(0, number_of_names)]


def _get_login(name: str):
    """Return user login by name"""
    return name.replace(' ', '_')


def _get_email(name):
    """Return user email by name"""
    local_part = name.replace(' ', '.').lower()
    domain = 'example.com'
    return f'{local_part}@{domain}'


def _get_project_key(project_keys):
    """Return random project key from a list"""
    return random.choice(project_keys) if project_keys else None
