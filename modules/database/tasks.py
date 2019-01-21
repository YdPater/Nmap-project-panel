from modules import db, app
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
            db.session.add(scan)
            db.session.commit()
    except KeyError:
        print("Target: {} gave an empty response! Is it up? If it is, try the -Pn option when scanning.".format(target))
