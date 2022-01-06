#!/usr/bin/env python3

import time
import json
import sqlite3
import requests

from typing import Union
from bs4 import BeautifulSoup
from datetime import date, datetime

COMMIT = False
CAN_APIKEY = "6af9022cc6464aeb9aec9fd499179327"

class FsuApiException(Exception):
    pass

def scrape_fsu_repcases():
    """Parses data from FSU's Business Intelligence"""

    print("Starting BI Request... (reported_cases)")

    # format data for fsu bi request
    headers = {
        "X-PowerBI-ResourceKey": "3d4d6287-74e7-42a1-9d8a-fdbfb66356e6"
    }
    with open("tools/assets/bi_timeseries.json", 'r') as file:
        data = json.loads(file.read())

    # get the data from fsu
    print(" - Sending post...")
    bi_res = requests.post(
        "https://wabi-us-east2-c-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true",
        headers=headers,
        json=data
    )

    # check request was proper
    if bi_res.status_code != 200:
        raise FsuApiException(f"FSU data request failed with code: {bi_res.status_code}!")

    print(" - Got data!")

    # convert to dict
    bi_json = bi_res.json()

    # get what we want from the data
    dataset_res = bi_json['results'][0]['result']['data']['dsr']
    dataset_list = dataset_res['DS'][0]['PH'][0]['DM0']

    # open database connection
    print(" - Opening DB connection...")
    con = sqlite3.connect("fsu_covid.sqlite3")
    cur = con.cursor()

    # iterate thru set and format data
    print(" - Beginning iterations...")
    lastcasecnt = None
    for item in dataset_list:

        # set vars
        count = 0

        # if C has 2 values, means new value
        if len(item['C']) == 2:
            count = lastcasecnt = item['C'][1]

        # else if repeat
        elif "R" in item.keys():
            count = lastcasecnt

        # else, error out
        else:
            raise FsuApiException(f"Failed to parse response from BI!\n{item}")

        # get ts. its utc, so add 5 hours
        ts = int(item['C'][0] / 1000) + 18000 

        # =========================== #
        # By this point, we have data #
        # =========================== #

        # see if entry exists in database already
        search_res = cur.execute(
            "SELECT * FROM 'fsu.reported_cases' WHERE timestamp=:ts", 
            {
                "ts": ts
            }
        ).fetchall()

        # if something already exists...
        if len(search_res) > 0:

            # print
            #print(f" - Updating {ts} to {count}...")

            # update it!
            cur.execute(
                "UPDATE 'fsu.reported_cases' SET timestamp=:ts, count=:cnt WHERE id=:id", 
                {
                    "id": search_res[0][0],
                    "ts": ts,
                    "cnt": count
                }
            )

        # otherwise, insert into!
        else:

            # print
            _t = datetime.fromtimestamp(ts)
            print(f" - Inserting {ts} ({_t.isoformat()})...")

            # update it!
            cur.execute(
                "INSERT INTO 'fsu.reported_cases' (timestamp, count) VALUES (:ts, :cnt)", 
                {
                    "ts": ts,
                    "cnt": count
                }
            )
    
    # close db
    print(" - Closing DB connection...")
    if COMMIT:
        con.commit()
    con.close()
    return

def scrape_fsu_estimates():
    """Parses data from FSU's Business Intelligence"""

    print("Starting BI Request... (estimates)")

    # format data for fsu bi request
    headers = {
        "X-PowerBI-ResourceKey": "6f459d49-93cf-4180-a719-66780515ea87"
    }
    with open("tools/assets/bi_estimates.json", 'r') as file:
        data = json.loads(file.read())

    # get the data from fsu
    print(" - Sending post...")
    bi_res = requests.post(
        "https://wabi-us-east2-c-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true",
        headers=headers,
        json=data
    )

    # check request was proper
    if bi_res.status_code != 200:
        raise FsuApiException(f"FSU data request failed with code: {bi_res.status_code}!")

    print(" - Got data!")

    # convert to dict
    bi_json = bi_res.json()

    # get what we want from the data
    dataset_res = bi_json['results'][0]['result']['data']['dsr']
    dataset = dataset_res['DS'][0]['PH'][1]['DM1']
    stu_cc = dataset[0]['X'][0]['M0']
    stu_pos = dataset[0]['X'][1]['M0']
    emp_cc = dataset[1]['X'][0]['M0']
    emp_pos = dataset[1]['X'][1]['M0']
    qt_total = stu_cc+stu_pos+emp_cc+emp_pos

    # get date timestamp in utc
    ts = int(time.mktime(date.today().timetuple()))

    # open database connection
    print(" - Opening DB connection...")
    con = sqlite3.connect("fsu_covid.sqlite3")
    cur = con.cursor()

    # =========================== #
    # By this point, we have data #
    # =========================== #

    # see if entry exists in database already
    search_res = cur.execute(
        "SELECT * FROM 'fsu.estimates' WHERE timestamp=:ts", 
        {
            "ts": ts
        }
    ).fetchall()

    # if something already exists, dont handle
    if len(search_res) > 0:
        pass

    # otherwise, insert into!
    else:

        # print
        _t = datetime.fromtimestamp(ts)
        print(f" - Inserting {ts} ({_t.isoformat()})...")

        # update it!
        cur.execute(
            "INSERT INTO 'fsu.estimates' " +
            "(timestamp, student_ccs, student_pos, employee_ccs, employee_pos, total) " +
            "VALUES (:ts, :stu_cc, :stu_pos, :emp_cc, :emp_pos, :qt_total)", 
            {
                "ts": ts,
                "stu_cc": stu_cc,
                "stu_pos": stu_pos,
                "emp_cc": emp_cc,
                "emp_pos": emp_pos,
                "qt_total": qt_total
            }
        )
    
    # close db
    print(" - Closing DB connection...")
    if COMMIT:
        con.commit()
    con.close()
    return

def scrape_fsu_testing():

    print("Starting Page Scrape... (testing)")

    # get page
    print(" - Sending GET request...")
    page = requests.get("https://stayhealthy.fsu.edu/dashboard")

    # check request was proper
    if page.status_code != 200:
        raise FsuApiException(f"FSU data request failed with code: {page.status_code}!")

    # start bs4
    soup = BeautifulSoup(page.text, 'html.parser')
    tables = soup.find_all('tbody')

    # see if page still meets criteria
    if len(tables) != 2:
        raise FsuApiException(f"FSU data parsing failed, not 2 tables! Now {len(tables)}!")

    # open database connection
    print(" - Opening DB connection...")
    con = sqlite3.connect("fsu_covid.sqlite3")
    cur = con.cursor()

    # iterate thru the two tables:
    print(" - Beginning iterations...")
    startyear = datetime.now().year
    for table in tables:
        for tr in table.find_all('tr'):

            # get data
            data = tr.find_all('td')

            # parse dates
            t_dates = data[0].text.split(" - ")
            start = datetime.strptime(t_dates[0], "%B %d")
            end = datetime.strptime( t_dates[1], "%B %d")

            # add year data
            if end.month == 1 and start.month == 12:
                end = end.replace(year=startyear)
                start = start.replace(year=startyear-1)
                startyear -= 1
            else:
                end = end.replace(year=startyear)
                start = start.replace(year=startyear)

            # convert to gmt timestamps
            start_ts = int(time.mktime(start.timetuple()))
            end_ts = int(time.mktime(end.timetuple()))

            # parse everything else
            test_cnt = int(data[1].text.replace(",", ""))
            stu_pos = int(data[2].text)
            emp_pos = int(data[3].text)
            tot_pos = int(data[4].text)
            pos_rate = float(data[5].text.replace("%", ""))

            # =========================== #
            # By this point, we have data #
            # =========================== #

            # see if entry exists in database already
            search_res = cur.execute(
                "SELECT * FROM 'fsu.testing' WHERE start=:start", 
                {
                    "start": start_ts
                }
            ).fetchall()

            # if something already exists...
            if len(search_res) > 0:

                # print
                #print(f" - Updating {search_res[0][0]}...")

                # update it!
                cur.execute(
                    "UPDATE 'fsu.testing' " +
                    "SET start=:start, end=:end, test_count=:test_count, " +
                    "pos_student=:pos_student, pos_employee=:pos_employee, " +
                    "pos_total=:pos_total, pos_rate=:pos_rate " +
                    "WHERE id=:id", 
                    {
                        "id": search_res[0][0],
                        "start": start_ts,
                        "end": end_ts,
                        "test_count": test_cnt,
                        "pos_student": stu_pos,
                        "pos_employee": emp_pos,
                        "pos_total": tot_pos,
                        "pos_rate": pos_rate
                    }
                )

            # otherwise, insert into!
            else:

                # print
                _t = datetime.fromtimestamp(start_ts)
                print(f" - Inserting {start_ts} ({_t.isoformat()})...")

                # update it!
                cur.execute(
                    "INSERT INTO 'fsu.testing' " +
                    "(start, end, test_count, pos_student, pos_employee, pos_total, pos_rate) " +
                    "VALUES (:start, :end, :test_count, :pos_student, :pos_employee, :pos_total, :pos_rate)", 
                    {
                        "start": start_ts,
                        "end": end_ts,
                        "test_count": test_cnt,
                        "pos_student": stu_pos,
                        "pos_employee": emp_pos,
                        "pos_total": tot_pos,
                        "pos_rate": pos_rate
                    }
                )
        
    # close db
    print(" - Closing DB connection...")
    if COMMIT:
        con.commit()
    con.close()
    return

def scrape_leon_data():

    print("Starting API Update... (leon)")

    # get data from api
    print(" - Sending GET request...")
    can_data = requests.get(
        "https://api.covidactnow.org/v2/county/12073.timeseries.json" +
        f"?apiKey={CAN_APIKEY}"
    ).json()

    # open database connection
    print(" - Opening DB connection...")
    con = sqlite3.connect("fsu_covid.sqlite3")
    cur = con.cursor()

    # start with metrics
    print(" - Beginning metrics iterations...")
    for item in can_data['metricsTimeseries']:

        # get data in manageable format
        _ts = datetime.strptime(item['date'], "%Y-%m-%d")
        ts = int(time.mktime(_ts.timetuple()))
        ptr = item['testPositivityRatio']
        cpc = item['caseDensity']
        ir = item['infectionRate'] if item['infectionRate'] is not None else 0.0
        ir90 = item['infectionRateCI90'] if item['infectionRateCI90'] is not None else 0.0

        # this key is funky because it doesnt exist until halfway
        vac_ratio = 0.0
        if "vaccinationsCompletedRatio" in item.keys():
            vac_ratio = item['vaccinationsCompletedRatio'] if item['vaccinationsCompletedRatio'] is not None else 0.0

        # see if entry exists in db
        search_res = cur.execute(
            "SELECT * FROM 'leon.metrics' WHERE timestamp=:ts", 
            {
                "ts": ts
            }
        ).fetchone()

        # if exists, update
        if search_res is not None:

            # update it!
            cur.execute(
                "UPDATE 'leon.metrics' " +
                "SET timestamp=:ts, pos_test_ratio=:ptr, cases_per_capita=:cpc, " +
                "r_naught=:ir, r_naught_ci90=:ir90, vac_ratio=:vac_ratio " +
                "WHERE id=:id", 
                {
                    "id": search_res[0],
                    "ts": ts,
                    "ptr": ptr,
                    "cpc": cpc,
                    "ir": ir,
                    "ir90": ir90,
                    "vac_ratio": vac_ratio
                }
            )

        # else, insert it
        else:

            # print
            print(f"   - Inserting {item['date']} ({_ts.isoformat()})...")

            # update it!
            cur.execute(
                "INSERT INTO 'leon.metrics' " +
                "(timestamp, pos_test_ratio, cases_per_capita, r_naught, r_naught_ci90, vac_ratio) " +
                "VALUES (:ts, :ptr, :cpc, :ir, :ir90, :vac_ratio)", 
                {
                    "ts": ts,
                    "ptr": ptr,
                    "cpc": cpc,
                    "ir": ir,
                    "ir90": ir90,
                    "vac_ratio": vac_ratio
                }
            )

    # now onto actuals
    print(" - Beginning actuals iterations...")
    for item in can_data['actualsTimeseries']:

        # get data in manageable format
        _ts = datetime.strptime(item['date'], "%Y-%m-%d")
        ts = int(time.mktime(_ts.timetuple()))
        tc = item['cases'] if item['cases'] is not None else 0
        td = item['deaths'] if item['deaths'] is not None else 0
        nc = item['newCases'] if item['newCases'] is not None else 0
        nd = item['newDeaths'] if item['newDeaths'] is not None else 0

        # this key is funky because it doesnt exist until halfway
        vac_cnt = 0
        if "vaccinationsCompleted" in item.keys():
            vac_cnt = item['vaccinationsCompleted'] if item['vaccinationsCompleted'] is not None else 0

        # see if entry exists in db
        search_res = cur.execute(
            "SELECT * FROM 'leon.actuals' WHERE timestamp=:ts", 
            {
                "ts": ts
            }
        ).fetchone()

        # if exists, update
        if search_res is not None:

            # update it!
            cur.execute(
                "UPDATE 'leon.actuals' " +
                "SET timestamp=:ts, total_cases=:tc, total_deaths=:td, " +
                "new_cases=:nc, new_deaths=:nd, vac_count=:vac_cnt " +
                "WHERE id=:id", 
                {
                    "id": search_res[0],
                    "ts": ts,
                    "tc": tc,
                    "td": td,
                    "nc": nc,
                    "nd": nd,
                    "vac_cnt": vac_cnt
                }
            )

        # else, insert it
        else:

            # print
            print(f"   - Inserting {item['date']} ({_ts.isoformat()})...")

            # update it!
            cur.execute(
                "INSERT INTO 'leon.actuals' " +
                "(timestamp, total_cases, total_deaths, new_cases, new_deaths, vac_count) " +
                "VALUES (:ts, :tc, :td, :nc, :nd, :vac_cnt)", 
                {
                    "ts": ts,
                    "tc": tc,
                    "td": td,
                    "nc": nc,
                    "nd": nd,
                    "vac_cnt": vac_cnt
                }
            )

    # close db
    print(" - Closing DB connection...")
    if COMMIT:
        con.commit()
    con.close()
    return

def main():
    scrape_fsu_repcases()
    scrape_fsu_estimates()
    scrape_fsu_testing()
    scrape_leon_data()

if __name__ == "__main__":
    exit(main())