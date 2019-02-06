import nmap
from modules import app
from modules.database.tasks import save_scandata
from modules.file_handler import delete_file
from os.path import join


def run_scan(target, arguments):
    nm = nmap.PortScanner()
    scaninfo = nm.scan(hosts=target, arguments=arguments)
    return scaninfo['scan']


def normal_scan(target, arguments, current_project):
    results = run_scan(target, arguments)
    save_scandata(results, target, current_project)
    print("Scan done!")


def run_list_scan(arguments, current_project, filename):
    with open(join(app.config['UPLOAD_FOLDER'], filename), 'r') as targetsfile:
        for target in targetsfile:
            target = target.strip()
            if target == "localhost":
                target = "127.0.0.1"
            results = run_scan(target, arguments)
            save_scandata(results, target, current_project)
    delete_file(filename)
    print("List scan done!")


def parse_arguments(service=None, ping=None):
    arguments = "T4 "
    if service:
        arguments += "-sV "
    if ping:
        arguments += "-Pn "
    return arguments


def parse_target(target):
    if target == "localhost":
        target = "127.0.0.1"
    return target