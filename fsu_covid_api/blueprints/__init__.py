import time
import sqlite3

from flask import Blueprint, Response, request, g

from ..modules.api_models import ApiError
from ..modules.db_models import UserData

# static vars
DB_PATH = "./fsu_covid.sqlite3"
RL_SEC = 5 * 60  # 5 minutes

# initialize api blueprint
api = Blueprint("api", __name__)

@api.before_request
def before_request():
    """Handles opening database connections, verifying API keys/ratelimits, and logging"""

    # initialize DB connection
    g.db = sqlite3.connect(DB_PATH)

    # get api key
    apikey = request.args.get('apikey')

    # if no apikey, return
    if not apikey:
        return ApiError(
            403,
            "Not Authorized",
            "Please provide an api key as query param 'apikey'."
        ).to_response()

    # see if apikey is within database
    cur = g.db.cursor()
    _udata = cur.execute(
        "SELECT * FROM 'users.data' WHERE apikey=:apikey",
        {
            "apikey": apikey
        }
    )

    # if no user data found, return
    if not _udata:
        return ApiError(
            403,
            "Not Authorized",
            "Your API Key is invalid. Please provide a valid api key."
        ).to_response()
    
    # else, convert to object
    udata = UserData(_udata.fetchone())

    # see if the user is within their ratelimit
    curtime = int(time.time())
    tlimit = curtime - RL_SEC
    rcount = cur.execute(
        "SELECT COUNT(*) FROM 'users.logs' WHERE user_id=:uid AND timestamp>:tlimit",
        {
            "uid": udata.id,
            "tlimit": tlimit
        }
    ).fetchone()

    # if surpassing rate limit, return
    if rcount[0] > udata.ratelimit:
        return ApiError(
            429,
            "Too Many Requests",
            f"You are being rate limited. You are currently allowed to make {udata.ratelimit} " +
            f"requests within any {RL_SEC} second period. Please wait and try again."
        ).to_response()
    
    # if we're here, we're clear!
    # add log into db and hand off
    cur.execute(
        "INSERT INTO 'users.logs' "+
        "(timestamp, user_id, query) "+
        "VALUES (:ts, :uid, :query)",
        {
            "ts": curtime,
            "uid": udata.id,
            "query": request.endpoint
        }
    )

@api.after_request
def after_request(res):
    """Handles closing database connection for each request"""

    # gracefully commit and close DB connection
    g.db.commit()
    g.db.close()

    # return response
    return res

@api.route("/", methods=["GET"])
def index():
    return "Hello!"

# import all other paths
from . import fsu
from . import leon
from . import main
