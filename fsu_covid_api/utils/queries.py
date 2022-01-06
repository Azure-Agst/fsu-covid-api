from flask import g
from ..modules.db_models import FSUEstimate, FSUPopulation, FSUReportedCases, \
    FSUTestingReport, LeonMetrics, LeonActuals

def db_fsu_latest_est():

    # set up cursor
    cur = g.db.cursor()

    # get latest estimate
    _estimate = cur.execute(
        "SELECT * FROM 'fsu.estimates' ORDER BY timestamp DESC LIMIT 1"
    )
    estimate = FSUEstimate(_estimate.fetchone())

    # get current population
    _population = cur.execute(
        "SELECT * FROM 'fsu.population' ORDER BY year DESC LIMIT 1"
    )
    population = FSUPopulation(_population.fetchone())

    # return dict
    return {
        "population":{
            "year": population.year,
            "students": population.students,
            "employees": population.employees,
            "total": population.total,
        },
        "students": {
            "positive": estimate.student_pos,
            "close_contacts": estimate.student_cc,
        },
        "employees": {
            "positive": estimate.employee_pos,
            "close_contacts": estimate.employee_cc,
        },
        "total_quarantined": estimate.total,
        "positivity_rate": round(estimate.total/population.total, 3),
        "last_updated": estimate.timestamp.strftime("%Y-%m-%d")
    }

def db_fsu_latest_testrept():

    # set up cursor
    cur = g.db.cursor()

    # get latest estimate
    _testreport = cur.execute(
        "SELECT * FROM 'fsu.testing' ORDER BY end DESC LIMIT 1"
    )
    testreport = FSUTestingReport(_testreport.fetchone())

    # return dict
    return {
        "start": testreport.start.strftime("%Y-%m-%d"),
        "end": testreport.end.strftime("%Y-%m-%d"),
        "total_tests": testreport.test_count,
        "students": {
            "positive": testreport.student_pos,
        },
        "employees": {
            "positive": testreport.employee_pos,
        },
        "total_positives": testreport.total_pos,
        "positivity_rate": testreport.pos_rate,
    }

def db_fsu_latest_reptcases():

    # set up cursor
    cur = g.db.cursor()

    # get latest case disclosure
    _latestcases = cur.execute(
        "SELECT * FROM 'fsu.reported_cases' ORDER BY timestamp DESC LIMIT 1"
    )
    latestcases = FSUReportedCases(_latestcases.fetchone())

    # get sum of all disclosures
    _sum = cur.execute(
        "SELECT SUM(count) FROM 'fsu.reported_cases'"
    )
    total_cases = _sum.fetchone()[0]

    # return dict
    return {
        "last_updated": latestcases.timestamp.strftime("%Y-%m-%d"),
        "new_cases": latestcases.count,
        "total": total_cases
    }

def db_leon_latest_metrics():

    # set up cursor
    cur = g.db.cursor()

    # get latest metrics where values are legit
    _latestmetrics = cur.execute(
        "SELECT * FROM 'leon.metrics' " +
        "WHERE (pos_test_ratio IS NOT NULL AND cases_per_capita IS NOT NULL) " +
        "ORDER BY timestamp DESC LIMIT 1"
    )
    latestmetrics = LeonMetrics(_latestmetrics.fetchone())

    # return dict
    return {
        "last_updated": latestmetrics.timestamp.strftime("%Y-%m-%d"),
        "positivity_rate": latestmetrics.pos_test_ratio,
        "cases_per_100k": latestmetrics.cases_per_capita,
        "r_naught": latestmetrics.r_naught,
        "r_naught_ci90": latestmetrics.r_naught_ci90,
        "vaccination_ratio": latestmetrics.vac_ratio,
    }

def db_leon_latest_actuals():

    # set up cursor
    cur = g.db.cursor()

    # get latest metrics where values are legit
    _latestmetrics = cur.execute(
        "SELECT * FROM 'leon.actuals' ORDER BY timestamp DESC LIMIT 1"
    )
    latestmetrics = LeonActuals(_latestmetrics.fetchone())

    # return dict
    return {
        "last_updated": latestmetrics.timestamp.strftime("%Y-%m-%d"),
        "total_cases": latestmetrics.total_cases,
        "total_deaths": latestmetrics.total_deaths,
        "new_cases": latestmetrics.new_cases,
        "new_deaths": latestmetrics.new_deaths,
        "vac_count": latestmetrics.vac_count,
    }
