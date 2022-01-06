from . import api
from ...modules.api_models import ApiResponse
from ...utils.queries import db_leon_latest_actuals, db_leon_latest_metrics, \
    db_fsu_latest_est, db_fsu_latest_testrept, db_fsu_latest_reptcases

@api.route("/all.json")
def get_all_stats():
    """Gets all available Stats"""

    # set up dict
    data = {}

    # add latest reported cases to dict
    data['fsu.reported_cases'] = db_fsu_latest_reptcases()

    # add latest estimate to dict
    data['fsu.estimates'] = db_fsu_latest_est()

    # add latest testing report to dict
    data['fsu.testing'] = db_fsu_latest_testrept()

    # add leon metrics to dict
    data['leon.metrics'] = db_leon_latest_metrics()

    # add leon actuals cases to dict
    data['leon.actuals'] = db_leon_latest_actuals()

    # return formatted response
    return ApiResponse(data).to_response()