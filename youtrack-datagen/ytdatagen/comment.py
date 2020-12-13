from datetime import datetime
import copy
import random

from ytdatagen.config import COMMENT_PROBABILITY, DT_FMT
from ytdatagen import utils


def bind2issues(issues, comments):
    """Bind comments to issues"""
    issues_with_comments = copy.deepcopy(issues)
    c2i = {}
    for i, comm in enumerate(comments):
        key = f'{comm["projectKey"]}-{comm["issueNumber"]}'
        if key not in c2i.keys():
            c2i[key] = [i]
        else:
            c2i[key].append(i)

    for iss in issues_with_comments:
        key = f'{iss["projectKey"]}-{iss["issueNumber"]}'
        if key in c2i.keys():
            issue_comments = []
            for i in c2i[key]:
                issue_comments.append({
                    k: v for k, v in comments[i].items() if k in ['commentAuthor', 'commentCreated', 'commentText']
                })
            iss['issueComments'] = issue_comments

    return issues_with_comments


def get(issues, users_by_project, probability=COMMENT_PROBABILITY):
    """Get list of comments"""
    comments = []

    for iss in issues:
        project_key = iss['projectKey']

        if random.random() < probability:
            for i in range(0, random.randint(0, 3)):
                author_name = random.choice(users_by_project[project_key])
                timestamp = utils.get_random_date(
                    datetime.strptime(iss['issueCreated'], DT_FMT),
                    datetime.strptime(iss['issueUpdated'], DT_FMT)
                ).strftime(DT_FMT)

                comm = {
                    "projectKey": project_key,
                    "issueNumber": iss['issueNumber'],
                    "commentAuthor": author_name,
                    "commentCreated": timestamp,
                    "commentText": _get_comment_text(),
                }
                comments.append(comm)

    return comments


def _get_comment_text():
    """Get random comment text from pre-defined set"""
    comment_samples = [
        "Malesu mauris nas lum rfusce vehicula bibend. Morbi.",
        "Nuncsed quamal felis donec rutrum class ipsumnam teger. Sedin metusd metusdo quamnunc utcras facilis nequen.",
        "Adipisci ent neque eger vehicula dis. Miquis auctorpr quamphas purusp phasel duifusce parturi. Ris liberoa ligula lacini risus nean. Arcualiq cubilia aenean nuncnunc ulum fringi uisque abitur rerit setiam. Nean miproin aliquet risusvi tempusp aliquete. Integer nequenu bulum ibulum laoree accumsan ellus mus odio uis. Amet curae ivamus congue aliquama liberofu que.",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In justov volutpat mus habitas dapibusc nequenu volutp justo. Quam blandi tur maurisd egesta erossed morbi turpis risus tate. Lacusp facilis class vehicula varius iaculis setiam montes pharetra. Usce ecenas quispr naeos nec nibhphas lacinia roin. Abitur maurisma metusqui justop uscras llam enas. Magnaqu faucibus sduis arcualiq imperd teger egetlor teger.",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Conseq tristiq enas duis sociosqu eduis enimsed tudin vel. Lus semnunc risusm nulla parturi atein at placerat. Tiam laut nibhnul turpisn vitaenul eleifen commodo euismo quat posuered. Egestas nullain justop maurisin purusp donec nas liberofu aptent. Nec aliquam tiam puruscra turpisp luctus proin. Lectusin turpisn usce orcivest nullam eget arcuduis tdonec min. Esent cursus vulput aenean bulum lacini congued pretiu. Portamor bulum tate isse llam cidunt estmae.\n\nSque leocras fusce nullap fusce convall laoreet nibhnull estsusp. Roin aliquet esent ctetur blandit etiam nequesed viverr. Nislqu sse orciduis lacusp in tasse gravida lla ullam. Itnunc id mauris rerit entum disse lacinia. Oin luctus velit musetiam onec potenti ipsump volutp. Tortor musetiam bibendum onec esent libero esque sim. Enas ras eclass placerat sedin risusut vulput enimdon montes. Rhoncus dolorma estsusp facilis etsed llaut esque cursus. Nisl ullamcor tincid llus nulla iaculis.",
    ]
    return random.choice(comment_samples)
