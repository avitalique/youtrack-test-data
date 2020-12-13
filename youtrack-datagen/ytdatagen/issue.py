from datetime import datetime
import random
import requests

from ytdatagen.config import DT_FMT, \
    ASSIGNEE_PROBABILITY, DESCRIPTION_PROBABILITY, LINK_PROBABILITY, NORMAL_PRIORITY_PROBABILITY
from ytdatagen import utils


def get(projects, users_by_project, issue_count_by_project, starting_number=1):
    """Generate list of issues"""

    issues = []
    for proj in projects:
        existing_links = {}
        key = proj['projectKey']
        summary_list = _get_summary_list()
        created_timestamps = utils.get_datetime_list(issue_count_by_project[key])
        for number_in_project in range(0, issue_count_by_project[key]):
            iss = {
                'issueNumber': number_in_project + starting_number,
                'projectKey': key,
                'projectName': proj['projectName'],
                'issueSummary': random.choice(summary_list),
                'issueReporterName': random.choice((users_by_project[key])),
                'issueCreated': created_timestamps[number_in_project].strftime(DT_FMT),
                'issueUpdated': None,
                'issueResolved': None,
                'issueTags': None,
                'issuePriority': _get_priority(),
                'issueType': _get_type(),
                'issueState': _get_state(),
                'issueAssignee': _get_assignee((users_by_project[key])),
                'issueSubsystem': _get_subsystem(),
                'issueFixVersions': _get_fix_version(),
                'issueAffectedVersions': _get_affected_versions(),
                'issueFixedInBuild': _get_fixed_in_build(),
                'issueDescription': _get_description(),
                'issueVotes': _get_votes(),
            }

            # Set issueUpdated and issueResolved fields
            if iss['issueState'] == 'Submitted':
                iss['issueUpdated'] = iss['issueCreated']
            else:
                iss['issueUpdated'] = utils.get_random_date(
                    datetime.strptime(iss['issueCreated'], DT_FMT),
                    datetime.now()
                ).strftime(DT_FMT)
                if iss['issueState'] in ['Fixed', 'Obsolete', 'Verified']:
                    iss['issueResolved'] = iss['issueUpdated']

            # Add links
            links = _get_links(
                iss['issueNumber'],
                range(starting_number, issue_count_by_project[key] + starting_number),
                existing_links
            )
            if links:
                existing_links[iss.get('issueNumber')] = [ln['targetIssueNumber'] for ln in links]

            iss['issueLinks'] = links

            # Append issue to the list
            issues.append(iss)

    return issues


#
def count_by_project(project_keys, total_issues):
    """Return a map of issue count by project"""
    issues_by_project = {}
    project_keys = list(project_keys)
    for k in project_keys:
        issues_by_project[k] = 0
    # print(issues_per_project)

    for i in range(0, total_issues):
        p = random.choice(project_keys)
        issues_by_project[p] += 1
    # print(issues_per_project)

    m = total_issues // len(project_keys) // 5
    for j in range(0, len(project_keys) // 2):
        diff = random.randint(m, m * 3)
        key1, key2 = project_keys[j], project_keys[-1 - j]
        issues_by_project[key1] += diff
        issues_by_project[key2] -= diff

    return issues_by_project


def _get_summary_list():
    """Return a list of random strings from http://names.drycodes.com"""
    r = requests.get(
        f'http://names.drycodes.com/1000?combine=4&separator=space'
    )
    return r.json()


def _get_description(probability=DESCRIPTION_PROBABILITY):
    """Return an issue description"""
    if random.random() < probability:
        description = "" \
                      "Nulla ris ullamco portado ultricie esque. Aliquam sduis purusp lum tortor quamal dapibusc metus aptent. Auctorpr aenean hendrer ecenas dictumst laoree. Estmae lectusa miquis bulum lla aenean congue magna sduis laoreet. Quat aesent setiam eratfus nulla facilis vitae. Teger puruscra turpis ullamcor laoreet tsed rsed esque dictumst. Placerat rutrum aenean orci cursusp oin elemen. Platea quamphas tdonec teger nisl usce nulla sceleris liberom mauris. Lobortis viverra arcuduis nislnam iquam hendrer bibendu magnis aliqua. Oin ibulum eratetia vitae ligulam ridicul esent duifusce.\n\nAccums idnulla antenull nec sagittis platea daut netus ibulum nequeal. Iumsed miquis sedinteg blandit suscip euismo. Que enulla class pellent llaut aliquet posuere rerit. Proin faucib ligulam at ras arcualiq egesta. Pretiu felis ger lobortis dapibusc lobortis quispr quamve malesu. Musetiam massan magnaqu egesta congued unc. Enimdon nislqu urnavest mus bibend ger facilisi nam nean. Cras quamve enim ulum uam nullain gsed nuncproi. Quamal rissed nulla urient enim duis ies asin facilisi. Faucibus lus liberom nunc cidunt euismo egetal lacusnam.\n\nSnam aesent que dolordo facilis turpisf auris llam morbi faucibus. Bibendu nibhnul sed scras ornare sociis malesuad velitsed. Ornareve maurisve lobortis orciduis ger ante eu arcualiq. Semper arcuduis llam platea facili maurisin erdiet egestas. Elit isque esent lectus praesent egestas aenean hac. Nec faucibu velitsed duis lectusin sellus nullam taciti. Eunulla congue lectuss lla ibulum odiophas. Ger dis commodo metusd miin nuncproi bibendu.\n\nSed tristi ger loremn tur vestib fusce volutpa. Lacusp sapiendo nec lobortis sapienv purusd faucibus elementu temporin suscip. Orem himena lacusp potenti viverr erdum nibhnul. Nullain netus turpisut massa ndisse tortorp daut lobortis. Lectus dictumst tate magnap egestas portamor nullain magnaves. Quamve aptent accumsan lectusa sduis massama semper duis tcras. Enean faucibu ger afusce magnapro ibulum ulum isised massan. Isse ipsumma enimdon imperd himena magnaqu naeos nislnam.\n\nNequeal ipsumves amus rsed orciut bulum vulput quamphas tortor. Iennam egesta pulvina interdum euismo malesu faucibus. Oin rutruma usce posuered ipsum llus convalli. Imperd nonmorbi nec rutrum ger netus tur lacusnam vestibu consequa. Rutruma massacra dapibus dumin leocras aliquama aenean felisut teger elementu. Ac egetlor pharetr sedin ulum risque tempusp justo mstut purus. Urnavest erdum varius feugiatm euismodd ridicul. Sellus cras liquam auris onec congue." \
                      ""
        return description
    else:
        return None


def _get_tags():
    """Return issue tags"""
    return None


def _get_priority(probability=NORMAL_PRIORITY_PROBABILITY):
    """Return issue priority"""
    if random.random() < probability:
        return 'Normal'
    else:
        return random.choice([
            'Show-stopper',
            'Critical',
            'Major',
            'Normal',
            'Minor',
        ])


def _get_type():
    """Return issue type"""
    return random.choice([
        'Bug',
        'Cosmetics',
        'Exception',
        'Feature',
        'Task',
        'Usability Problem',
        'Performance Problem',
        'Epic',
    ])


def _get_state():
    """Return issue state"""
    return random.choice([
        'Submitted',
        'Open',
        'In Progress',
        'Fixed',
        'Obsolete',
        'Verified',
    ])


def _get_assignee(names, probability=ASSIGNEE_PROBABILITY):
    """Randomly return `Unassigned` or an assignee name from input names list"""
    if random.random() < probability:
        return random.choice(names)
    else:
        return None  # 'Unassigned'


def _get_subsystem():
    """Return a default value for `Subsystem` field"""
    return None  # 'No Subsystem'


def _get_fix_version():
    """Return a default value for `Fix versions` field"""
    return None  # 'Unscheduled'


def _get_affected_versions():
    """Return a default value for `Affected versions` field"""
    return None  # 'Unknown'


def _get_fixed_in_build():
    """Return a default value for `Fixed in build` field"""
    return None  # 'Next Build'


def _get_votes():
    """Return a default number of issue votes"""
    return 0


def _get_links(current_number, number_range, existing_links, max_links=3, probability=LINK_PROBABILITY):
    """Return a list of issue links"""
    links = {}
    if random.random() < probability:
        for i in range(random.randint(1, max_links)):
            target = random.choice(number_range)
            if existing_links.get(target):
                target_links = existing_links.get(target)
            else:
                target_links = []
            if (target != current_number) and (target not in links.keys()) and (current_number not in target_links):
                links[target] = _get_link_type()
    links = [{'linkType': v, 'targetIssueNumber': k} for k, v in links.items()]
    return links


def _get_link_type():
    """Return link type"""
    return random.choice(['Relates'])
