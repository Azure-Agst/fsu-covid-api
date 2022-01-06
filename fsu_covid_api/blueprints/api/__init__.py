import time
import sqlite3

from flask import Blueprint, request, g

from ...modules.api_models import ApiError
from ...modules.db_models import UserData

# static vars
DB_PATH = "./fsu_covid.sqlite3"
RLIM_WIN = 5 * 60  # 5 minutes
RLIM_IPCNT = 25  # 25 attempts

# initialize api blueprint
api = Blueprint("api", __name__)

def handle_ip_ratelimit():

    # useful vars
    ip = request.remote_addr
    timeout = int(time.time()) - RLIM_WIN # now, minus rate limit window

    # check if ip is being annoying first
    cur = g.db.cursor()
    ip_req_count = cur.execute(
        "SELECT COUNT(*) FROM 'users.canaries' WHERE ip=:ip AND timestamp>:time",
        {
            "ip": ip,
            "time": timeout
        }
    ).fetchone()[0]

    # if they're being annoying, return rate limit
    if ip_req_count > 25:
        return ApiError(
            429,
            "Too Many Requests",
            f"Your IP is being rate limited. Your IP is currently allowed to make {RLIM_IPCNT} " +
            f"requests within any {RLIM_WIN} second period. Please wait and try again."
        ).to_response()

def handle_apikey(apikey):

    # check ip first
    _ipres = handle_ip_ratelimit()
    if _ipres is not None:
        return _ipres

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
    tlimit = curtime - RLIM_WIN
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
            f"Your API key is being rate limited. You are currently allowed to make {udata.ratelimit} " +
            f"requests within any {RLIM_WIN} second period. Please wait and try again."
        ).to_response()
    
    # if we're here, we're clear!
    # add log into db and hand off
    cur.execute(
        "INSERT INTO 'users.logs' "+
        "(timestamp, user_id, ip, query) "+
        "VALUES (:ts, :uid, :ip, :query)",
        {
            "ts": curtime,
            "uid": udata.id,
            "ip": request.remote_addr,
            "query": request.endpoint
        }
    )

def handle_canary(canary):

    # check ip first
    _ipres = handle_ip_ratelimit()
    if _ipres is not None:
        return _ipres

    # first, do some cleanup
    curtime = int(time.time())
    deltime = curtime - (10 * 60) # 10 minutes
    cur = g.db.cursor()
    cur.execute(
        "DELETE FROM 'users.canaries' WHERE timestamp<:deltime",
        {
            "deltime": deltime
        }
    )

    # see if canary is within database
    print(canary)
    canarydata = cur.execute(
        "SELECT * FROM 'users.canaries' WHERE canary=:canary",
        {
            "canary": canary
        }
    ).fetchone()

    # if no result, return error
    if not canarydata:
        return ApiError(
            403,
            "Not Authorized",
            "We encountered an error processing your request. Please refresh the page. 1"
        ).to_response()
    
    # if IP addresses are different
    if canarydata[2] != request.remote_addr:
        return ApiError(
            403,
            "Not Authorized",
            "We encountered an error processing your request. Please refresh the page. 2"
        ).to_response()

    # if here, we're good
    # remove canary from db
    cur.execute(
        "DELETE FROM 'users.canaries' WHERE canary=:canary",
        {
            "canary": canary
        }
    )

    # add log entry
    cur.execute(
        "INSERT INTO 'users.logs' "+
        "(timestamp, canary, ip, query) "+
        "VALUES (:ts, :canary, :ip, :query)",
        {
            "ts": curtime,
            "canary": canary,
            "ip": request.remote_addr,
            "query": request.endpoint
        }
    )


@api.before_request
def before_request():
    """Handles opening database connections, verifying API keys/ratelimits, and logging"""

    # initialize DB connection
    g.db = sqlite3.connect(DB_PATH)

    # get useful vars
    ip = str(request.remote_addr)

    # get api key
    apikey = request.args.get('apikey')
    canary = request.args.get('canary')

    # if apikey, handle
    if apikey:

        # pass to subfunction
        return handle_apikey(apikey)

    # else if canary
    elif canary:

        # pass to subfunction
        return handle_canary(canary)

    else:
        return ApiError(
            403,
            "Not Authorized",
            "Please provide an api key as query param 'apikey'."
        ).to_response()

    

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
