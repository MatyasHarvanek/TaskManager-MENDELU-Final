import bcrypt
import loginHelper
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import db

app = Flask(__name__)
app.secret_key = "supertajny"


@app.route("/")
def home():
    return render_template("shared.html", tasks=db.get_tasks_without_user())


@app.route("/add-shared",  methods=['GET', 'POST'])
def add_shared():
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        db.create_task(name=name, description=description, user_id=None)
        return redirect(url_for('home'))
    return render_template("add-shared.html")


@app.route("/personal")
def personal():
    if not loginHelper.isUserLogedIn(session=session):
        return redirect(url_for('home'))

    return render_template("personal.html", tasks=db.get_user_tasks(session['id']))


@app.route("/add-personal", methods=['GET', 'POST'])
def add_personal():
    if not loginHelper.isUserLogedIn(session=session):
        print("test from this fucking shit")
        return redirect(url_for('home'))
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        db.create_task(name=name, description=description,
                       user_id=session['id'])
        return redirect(url_for('personal'))
    return render_template("add-personal.html")


@app.route("/done/<int:task_id>", methods=['GET'])
def done(task_id):
    db.mark_task_as_done(task_id=task_id)
    return redirect(url_for('home'))


@app.route("/history")
def history():
    if not loginHelper.isUserLogedIn(session=session):
        return redirect(url_for('home'))

    history = db.get_history(session['id'])
    return render_template('history.html', tasks=history)


@app.route("/undone/<int:task_id>", methods=['GET'])
def undone(task_id):
    db.mark_task_as_undone(task_id=task_id)
    return redirect(url_for('home'))


@app.route("/donepersonal/<int:task_id>", methods=['GET'])
def donePersonal(task_id):
    db.mark_task_as_done(task_id=task_id, user_id=session['id'])
    return redirect(url_for('personal'))


@app.route("/undonepersonal/<int:task_id>", methods=['GET'])
def undonePersonal(task_id):
    db.mark_task_as_undone(task_id=task_id, user_id=session['id'])
    return redirect(url_for('personal'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        if loginHelper.isUserLogedIn(session=session):
            return redirect(url_for('home'))
        else:
            return render_template("login.html")
    else:
        user = db.get_user(request.form['name'])
        if user is None:
            return render_template("login.html", loginError="Uživatelské jméno nebo heslo je špatné")
        if not user['password'] == request.form["password"]:
            return render_template("login.html", loginError="Uživatelské jméno nebo heslo je špatné")

        # login has been valid
        sendUserInfo(userId=user['id'], name=user['name'])
        return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if loginHelper.isUserLogedIn(session=session):
            return redirect(url_for("home"))
        else:
            return render_template('register.html')

    LoginValid = loginHelper.isUserLoginValid(
        request.form["name"], request.form["password"])
    if LoginValid.isValid:
        db.create_user(request.form["name"], request.form["password"])
        dbUser = db.get_user(request.form["name"])
        sendUserInfo(userId=dbUser['id'], name=dbUser['name'])
        return redirect(url_for("home"))

    return render_template('register.html', error=LoginValid.message)


@app.route('/logoff')
def logoff():
    session.clear()
    return redirect(url_for('home'))


def sendUserInfo(userId, name):
    session['id'] = userId
    session['username'] = name


if __name__ == "__main__":
    app.run(debug=True)
