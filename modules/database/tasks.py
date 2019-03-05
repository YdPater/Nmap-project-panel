from modules.config import db, app
from modules.database.models import Scandata


def save_scandata(results, target, current_project):
    try:
        for key, value in results[target]['tcp'].items():
            port = key
            state = value['state']
            service = value['name']
            product = value['product']
            version = value['version']
            scan = Scandata(target, state, port, service, product, version, current_project.id, notes="")
            save_to_db(scan)
    except KeyError:
        print("Target: {} gave an empty response! Is it up? If it is, try the -Pn option when scanning.".format(target))


def authorise(uid, projectid, Invites, Projects):
    invited_pr = Invites.query.filter_by(uid=uid, project_id=projectid).first()
    if invited_pr is not None:
        if int(invited_pr.project_id) != int(projectid):
            return False
        current_project = Projects.query.filter_by(id=projectid).first()
        return current_project
    else:
        current_project = Projects.query.filter_by(creator=uid, id=projectid).first()
        if not current_project or uid != current_project.creator:
            return False
        return current_project


def save_to_db(object):
    db.session.add(object)
    db.session.commit()


def delete_from_db(object):
    db.session.delete(object)
    db.session.commit()