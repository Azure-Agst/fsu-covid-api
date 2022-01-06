from . import api
from ..modules.api_models import ApiResponse
from ..utils.queries import db_leon_latest_actuals, db_leon_latest_metrics

@api.route("/leon.json")
def get_all_leon_stats():
    """Gets all Leon Stats"""

    # set up dict
    data = {}

    # add leon metrics to dict
    data['leon.metrics'] = db_leon_latest_metrics()

    # add leon actuals cases to dict
    data['leon.actuals'] = db_leon_latest_actuals()

    # return formatted response
    return ApiResponse(data).to_response()

@api.route("/leon.metrics.json")
def get_leon_metrics():
    """Gets all Leon Stats"""

    # set up dict
    data = {}

    # add leon metrics to dict
    data['leon.metrics'] = db_leon_latest_metrics()

    # return formatted response
    return ApiResponse(data).to_response()

@api.route("/leon.actuals.json")
def get_leon_actuals():
    """Gets all Leon Stats"""

    # set up dict
    data = {}

    # add leon actuals cases to dict
    data['leon.actuals'] = db_leon_latest_actuals()

    # return formatted response
    return ApiResponse(data).to_response()
