import sqlite3
from datetime import datetime
from flask import Blueprint, render_template, g
from ..api import DB_PATH

# initialize webapp blueprint
webapp = Blueprint(
    "webapp", __name__,
    static_folder='static',
    template_folder='templates'
)

@webapp.before_request
def before_request():
    """Handles opening database connections"""

    # initialize DB connection
    g.db = sqlite3.connect(DB_PATH)

@webapp.after_request
def after_request(res):
    """Handles closing database connection for each request"""

    # gracefully commit and close DB connection
    g.db.commit()
    g.db.close()

    # return response
    return res

# initialize 404
@webapp.app_errorhandler(404)
def webapp_error404(e):
    return render_template(
        '404.html',
        date=datetime.now()
    ), 404

# import all of the paths
from . import index
