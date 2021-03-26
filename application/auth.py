import functools
import re 

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from application.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def check(email):  
    if(re.search(regex,email)):  
        return True 
    else:  
        return False

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        )


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        password_verify = request.form["password_verify"]
        init_tours = request.form["init_tours"]
        if init_tours == "":
            init_tours = 0
        db = get_db()
        error = None
        
        if "visible" in request.form:
            visible = 1
        else:
            visible = 0
        if not username:
            error = "Skriv inn et brukernavn."
        elif not password:
            error = "Skriv inn et passord."
        elif not email:
            error = "Skriv inn en E-Post adresse."
        elif password != password_verify:
            error = "Passordene er ikke like."
        elif not check(email):
            error = "Ugyldig E-Post adresse."
        elif (
            db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
            is not None
        ):
            error = "E-Posten '{0}' er i bruk.".format(email)

        try:
            int(init_tours)
        except:
            error = "'{}' er ikke et gyldig antall turer".format(init_tours)
        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            db.execute(
                "INSERT INTO users (username, password, email, visible, initial_tours) VALUES (?, ?, ?, ?, ?)",
                (username, generate_password_hash(password), email, visible, int(init_tours)),
            )
            db.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
