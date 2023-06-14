import bcrypt
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


mock_tasks = [
    {
        "id": 0,
        "name": "Vynést odpadky",
        "description": "Prosím, fakt prosím lidi 🗑️",
        "is_done": False,
    },
    {
        "id": 1,
        "name": "Vytřít podlahu",
        "description": "V koupelně je to fakt síla 🤢",
        "is_done": False,
    },
    {
        "id": 2,
        "name": "Koupit mléko 🥛",
        "description": "Došlo a už nemáme žádné další",
        "is_done": True,
    },
]


@app.route("/")
def home():
    print(db.get_tasks_without_user())
    return render_template("shared.html", tasks=db.get_tasks_without_user(), headerLinkURL=url_for("login"), headerLinkText="Přihlásit")

@app.route("/add-shared",  methods=['GET', 'POST'])
def add_shared():
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        db.create_task(name=name, description=description, user_id=None)
        return redirect(url_for('home'))
    return render_template("add-shared.html", headerLinkURL=url_for("home"), headerLinkText="Domů")

@app.route("/add-personal")
def add_personal():
    return render_template("add-personal.html", headerLinkURL=url_for("home"), headerLinkText="Domů")

@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == "GET":
        if session.get('id') and session.get('username'):
            return redirect(url_for('home'))
        else:
            return render_template("login.html", headerLinkURL=url_for("home"), headerLinkText="Domů")
    else:
        session['id'] = 1
        session['username'] = "jou"
        user = db.get_user(request.form['name'])
        if user is None:
            return render_template("login.html", headerLinkURL=url_for("home"), headerLinkText="Domů")
        else:
            if user['password'] == request.form["password"]:
                session['id'] = user['id']
                session['username'] = user['name']
        print("user info" + str(user['password']))
        return redirect(url_for('home'))






@app.route("/personal")
def personal():
    return render_template("personal.html", headerLinkURL=url_for("home"), headerLinkText="Domů")

@app.route("/done/<int:task_id>", methods=['GET'])
def done(task_id):
    db.mark_task_as_done(task_id=task_id)
    return redirect(url_for('home'))


@app.route("/undone/<int:task_id>", methods=['GET'])
def undone(task_id):

    print("test")
    db.mark_task_as_undone(task_id=task_id)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
