from modules import app, db
from flask import render_template, redirect, request, url_for, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from modules.database.models import User, Projects, Scandata, Invites
from modules.database.tasks import save_scandata
from modules.userforms.forms import LoginForm, RegistrationForm, Projectform, Scanform, Fileform, Updateform, Inviteform
from modules.nmap_script import run_scan
from modules.file_handler import save_file, delete_file
from os.path import join
import csv


def get_userprojects(uid):
    list = Projects.query.filter_by(creator=uid).all()
    return list


# Base route, login is required. This page shows the created projects for the
# current user.
@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    prlist = get_userprojects(current_user.id)
    invited_pr = Invites.query.filter_by(uid=current_user.id).all()
    invited_pr_data = []
    for project in invited_pr:
        pr = Projects.query.filter_by(id=project.project_id).first()
        invited_pr_data.append(pr)
    form = Projectform()
    # When the form posts to this route...
    if request.method == "POST":
        # Check if the form is valid
        if form.validate_on_submit():
            prname = form.projectname.data
            # Check if the projectname does not already exists
            if Projects.query.filter_by(naam=prname, creator=current_user.id).first():
                return render_template("home.html", form=form, message="exists", lijst=prlist)
            creator = current_user.id
            description = form.description.data
            # Create a new project and save it to the database
            project = Projects(prname, description, creator)
            db.session.add(project)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('home.html', form=form, message=False, lijst=prlist, lijst2=invited_pr_data)


@app.route("/home/<projectname>", methods=["GET", "POST"])
@login_required
def projectview(projectname):
    invited_pr = Invites.query.filter_by(uid=current_user.id, project_id=projectname).first()
    if invited_pr is not None:
        if int(invited_pr.project_id) != int(projectname):
            print('true')
            return render_template("error_pages/404.html")
        current_project = Projects.query.filter_by(id=projectname).first()
    else:
        current_project = Projects.query.filter_by(creator=current_user.id, id=projectname).first()
        if not current_project or current_user.id != current_project.creator:
            return render_template("error_pages/404.html")
    existing_scans = Scandata.query.filter_by(project_id=current_project.id).all()
    form = Scanform()
    fileform = Fileform()
    updateform = Updateform()
    inviteform = Inviteform()
    invitedusers = Invites.query.filter_by(project_id=projectname).all()
    inv_usr_list = []
    for user in invitedusers:
        inv_usr_list.append(User.query.filter_by(id=user.uid).first())
    if request.method == "POST":
        arguments = "-T4 "
        if form.validate_on_submit():
            if current_user.id != current_project.creator:
                return redirect(url_for('projectview', projectname=current_project.id))
            target = form.target.data
            service = form.service.data
            ping = form.ping.data
            if service:
                arguments += "-sV "
            if ping:
                arguments += "-Pn "
            if target == "localhost":
                target = "127.0.0.1"
            results = run_scan(target, arguments)
            save_scandata(results, target, current_project)
            return redirect(url_for('projectview', projectname=current_project.id))
        elif fileform.validate_on_submit():
            if current_user.id != current_project.creator:
                return redirect(url_for('projectview', projectname=current_project.id))
            targets = fileform.targetfile.data
            filename = save_file(targets)
            service = fileform.service.data
            ping = fileform.ping.data
            if service:
                arguments += "-sV "
            if ping:
                arguments += "-Pn "
            with open(join(app.config['UPLOAD_FOLDER'], filename), 'r') as targetsfile:
                for target in targetsfile:
                    target = target.strip()
                    if target == "localhost":
                        target = "127.0.0.1"
                    results = run_scan(target, arguments)
                    save_scandata(results, target, current_project)
            delete_file(filename)
            return redirect(url_for('projectview', projectname=current_project.id))
        elif updateform.validate_on_submit():
            if current_user.id != current_project.creator:
                return redirect(url_for('projectview', projectname=current_project.id))
            scanid = updateform.id.data
            note = updateform.note.data
            projectid = Scandata.query.filter_by(id=scanid).first()
            if not projectid:
                return render_template('projectview.html',
                                       project=current_project,
                                       form=form, form2=fileform,
                                       form3=updateform, scans=existing_scans,
                                       message="notexists", userlist=inv_usr_list)
            projects_owned = Projects.query.filter_by(creator=current_user.id).all()
            project_id_list = []
            for id in projects_owned:
                project_id_list.append(id.id)
            if projectid.project_id not in project_id_list:
                return render_template('projectview.html',
                                       project=current_project,
                                       form=form, form2=fileform,
                                       form3=updateform, scans=existing_scans,
                                       message="notyours", userlist=inv_usr_list)
            elif projectid.project_id != current_project.id:
                return render_template('projectview.html',
                                       project=current_project.naam,
                                       form=form, form2=fileform,
                                       form3=updateform, scans=existing_scans,
                                       message="wrongproject", userlist=inv_usr_list)

            Scandata.query.filter_by(id=scanid).update(dict(notes=note))
            db.session.commit()
            return redirect(url_for('projectview', projectname=current_project.id))
        elif inviteform.validate_on_submit():
            if current_user.id != current_project.creator:
                return render_template('/static/error_pages/404.html')
            email = inviteform.email.data
            invited_user = User.query.filter_by(email=email).first()
            if not invited_user:
                return render_template('projectview.html', project=current_project, form=form,
                                       form2=fileform, form3=updateform, form4=inviteform,
                                       scans=existing_scans, userlist=inv_usr_list)
            invites = Invites.query.filter_by(uid=invited_user.id).first()
            if current_user.id == invited_user.id or invites:
                return redirect(url_for('projectview', projectname=current_project.id))
            invite = Invites(current_project.id, invited_user.id)
            db.session.add(invite)
            db.session.commit()
            return redirect(url_for('projectview', projectname=current_project.id))
    return render_template("projectview.html", project=current_project,
                           form=form, form2=fileform, form3=updateform, form4=inviteform,
                           scans=existing_scans, userlist=inv_usr_list)


@app.route("/home/download/<projectname>")
def download_scanoutput(projectname):
    invited_pr = Invites.query.filter_by(uid=current_user.id, project_id=projectname).first()
    print(invited_pr)
    if invited_pr is not None:
        if int(invited_pr.project_id) != int(projectname):
            print('id not the same')
            return render_template("error_pages/404.html")
        current_project = Projects.query.filter_by(id=projectname).first()
    else:
        current_project = Projects.query.filter_by(creator=current_user.id, id=projectname).first()
        if not current_project or current_user.id != current_project.creator:
            print("id not the same without invite")
            return render_template("error_pages/404.html")
    user = current_user.id
    if current_project is None:
        print("empty project")
        return render_template("error_pages/404.html")
    existing_scans = Scandata.query.filter_by(project_id=current_project.id).all()
    results = []
    with open(join(app.config["OUTPUT_DIR"], "outfile-{}-{}.csv".format(current_project.naam, current_user.username)), "w") as outfile:
        writer = csv.writer(outfile, delimiter=',', quotechar='"')
        writer.writerow(['Target', 'State', 'Portnumber', 'Service', 'Product', 'Version', 'Notes'])
        for scan in existing_scans:
            writer.writerow([scan.target, scan.state, scan.port, scan.service,
                             scan.product, scan.version, scan.notes])
    return send_from_directory('static/writedir/', filename="outfile-{}-{}.csv".format(current_project.naam, current_user.username))


@app.route("/home/revoke/<projectname>/<uid>", methods=["POST"])
@login_required
def revoke_access(projectname, uid):
    current_project = Projects.query.filter_by(creator=current_user.id, id=projectname).first()
    if not current_project or current_user.id != current_project.creator:
        print("id not the same without invite")
        return render_template("error_pages/404.html")
    invite = Invites.query.filter_by(project_id=projectname, uid=uid).first()
    db.session.delete(invite)
    db.session.commit()
    return redirect(url_for('projectview', projectname=current_project.id))


@app.route("/home/delete/<projectname>")
@login_required
def delete_page(projectname):
    user = current_user.id
    project = Projects.query.filter_by(creator=user, id=projectname).first()
    if project is None or user != project.creator:
        return render_template("error_pages/404.html")
    results = Scandata.query.filter_by(project_id=project.id).all()
    invites = Invites.query.filter_by(project_id=project.id).all()
    for result in results:
        db.session.delete(result)
    for invite in invites:
        db.session.delete(invite)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None:
                return render_template("login.html", form=form, message='creds')
            if user.check_password(form.password.data):
                login_user(user)
                next = request.args.get('next')
                if next is None or not next[0] == '/':
                    next = url_for('home')
                return redirect(next)
            return render_template("login.html", form=form, message='creds')
        else:
            return render_template("login.html", form=form, message="email")

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            existing_user = User.query.filter_by(email=form.email.data).first()

            # Check if the submitted email doesn't already exist in the database
            if existing_user is not None and form.email.data == existing_user.email:
                return render_template('register.html', form=form, message="email")

            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login', message="success"))
        else:
            return render_template('register.html', form=form, message='wrong_fill')

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error_pages/404.html"), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template("error_pages/500.html"), 500


if __name__ == '__main__':
    app.run(host="localhost", debug=True)
