from . import api
from ..modules.api_models import ApiResponse
from ..utils.queries import db_fsu_latest_est, db_fsu_latest_testrept, db_fsu_latest_reptcases

@api.route("/fsu.json")
def get_all_fsu_stats():
    """Gets all FSU Stats"""

    # set up dict
    data = {}

    # add latest reported cases to dict
    data['fsu.reported_cases'] = db_fsu_latest_reptcases()

    # add latest estimate to dict
    data['fsu.estimates'] = db_fsu_latest_est()

    # add latest testing report to dict
    data['fsu.testing'] = db_fsu_latest_testrept()

    # return formatted response
    return ApiResponse(data).to_response()

@api.route("/fsu.reported_cases.json")
def get_fsu_reptcases_stats():
    """Gets FSU Reported Cases Stats"""

    # set up dict
    data = {}

    # add latest reported cases to dict
    data['fsu.reported_cases'] = db_fsu_latest_reptcases()

    # return formatted response
    return ApiResponse(data).to_response()

@api.route("/fsu.estimates.json")
def get_fsu_estimates_stats():
    """Gets FSU Estimated Quarantining Stats"""

    # set up dict
    data = {}

    # add latest reported cases to dict
    data['fsu.estimates'] = db_fsu_latest_est()

    # return formatted response
    return ApiResponse(data).to_response()

@api.route("/fsu.testing.json")
def get_fsu_testrept_stats():
    """Gets FSU Estimated Quarantining Stats"""

    # set up dict
    data = {}

    # add latest reported cases to dict
    data['fsu.testing'] = db_fsu_latest_testrept()

    # return formatted response
    return ApiResponse(data).to_response()
