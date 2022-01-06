import time
import uuid
from datetime import datetime
from flask import Blueprint, request, render_template, g
from ..api import DB_PATH
from . import webapp

@webapp.route("/")
@webapp.route("/index.html")
def index():

    # hacky. i should restructure this but i wont

    # gather data for event
    canary = str(uuid.uuid4())
    ip = str(request.remote_addr)
    now = int(time.time())

    # open db conn
    cur = g.db.cursor()

    # while we're here, delete all canaries over 5 minutes old
    cur.execute(
        "DELETE FROM 'users.canaries' WHERE timestamp<=:ts",
        {
            "ts": now - 300
        }
    )

    # add our canary
    cur.execute(
        "INSERT INTO 'users.canaries' "+
        "(timestamp, ip, canary) "+
        "VALUES (:ts, :ip, :canary)",
        {
            "ts": now,
            "ip": ip,
            "canary": canary
        }
    )

    # return our template with proper data
    return render_template(
        "index.html",
        canary=canary,
        date=datetime.now()
    ), 200
