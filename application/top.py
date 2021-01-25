from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from datetime import date

from application.auth import login_required
from application.db import get_db, get_user, get_user_tours_count, get_user_tours

bp = Blueprint("top", __name__)

@bp.route("/top")
def user_index(user_id):
    user = get_user(user_id)
    tour_count = get_user_tours_count(user_id,date.today().year)['count_tours']
  
    return render_template('user/user_index.html', user=user, tour_count=tour_count)
