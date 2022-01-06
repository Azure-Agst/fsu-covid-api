#!/usr/bin/env python3

import sqlite3
from datetime import datetime

def update_fsu_reportedcases():
    """Update fsu.reported_cases table"""

    # init db connection
    print("Opening DB connection...")
    con = sqlite3.connect("fsu_covid.sqlite3")
    cur = con.cursor()

    # get all entries
    _db_entries = cur.execute(
        "SELECT * FROM 'fsu.reported_cases'"
    )
    db_entries = _db_entries.fetchall()

    # print out for debug
    print(f"Got {len(db_entries)} entries!")

    # iterate over each entry
    for entry in db_entries:

        # check old timestamp
        # olddt = datetime.fromtimestamp(entry[1])
        # if olddt.hour == 0:
        #     print(f"skipping {entry[1]}")
        #     continue

        # compute new timestamp (+4:00:00)
        newts = entry[1] + 3600

        # print it out
        newts_str = datetime.fromtimestamp(newts).isoformat()
        print(f"Updating {entry[1]} to {newts} ({newts_str})")

        # update in database
        cur.execute(
            "UPDATE 'fsu.reported_cases' SET timestamp=:newts WHERE id=:id",
            {
                "newts": newts,
                "id": entry[0]
            }
        )

    # close db
    print("Closing DB connection...")
    con.commit()
    con.close()
    
def update_fsu_testing():
    """Update fsu.testing table"""

    # init db connection
    print("Opening DB connection...")
    con = sqlite3.connect("fsu_covid.sqlite3")
    cur = con.cursor()

    # get all entries
    _db_entries = cur.execute(
        "SELECT * FROM 'fsu.testing'"
    )
    db_entries = _db_entries.fetchall()

    # print out for debug
    print(f"Got {len(db_entries)} entries!")

    # iterate over each entry
    for entry in db_entries:

        # check old timestamps
        start_olddt = datetime.fromtimestamp(entry[1])
        end_olddt = datetime.fromtimestamp(entry[2])
        if start_olddt.hour == 0 and end_olddt.hour == 0:
            print(f"skipping {entry[1]}")
            continue
        else:
            pass
            #print(start_olddt.hour, end_olddt.hour)#

        # compute new timestamp (+4:00:00)
        s_newts = entry[1] + 3600
        e_newts = entry[2] + 3600

        # print it out
        s_newts_str = datetime.fromtimestamp(s_newts).isoformat()
        e_newts_str = datetime.fromtimestamp(e_newts).isoformat()
        print(f"Updating {entry[1]} to {s_newts} ({s_newts_str}, {e_newts_str})")

        # update in database
        cur.execute(
            "UPDATE 'fsu.testing' SET start=:snewts, end=:enewts WHERE id=:id",
            {
                "snewts": s_newts,
                "enewts": e_newts,
                "id": entry[0]
            }
        )

    # close db
    print("Closing DB connection...")
    con.commit()
    con.close()

def main():
    """
    This script only exists because I fucked up on the timestamps beforehand.
    This is my attempt to localize them.
    """

    # update this table
    update_fsu_reportedcases()

    # get all data from 
    pass

if __name__ == "__main__":
    exit(main())