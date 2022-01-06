from typing import Tuple
from datetime import datetime

class UserData:
    def __init__(self, db_data: Tuple):
        self.id = db_data[0]
        self.email = db_data[1]
        self.apikey = db_data[2]
        self.ratelimit = db_data[3]

class Annotation:
    def __init__(self, db_data: Tuple):
        self.id = db_data[0]
        self.src_table = db_data[1]
        self.name = db_data[2]
        self.url = db_data[3]
        self.notes = db_data[4]

class FSUEstimate:
    def __init__(self, db_data: Tuple):
        self.id = db_data[0]
        self.timestamp = datetime.fromtimestamp(db_data[1])
        self.student_cc = db_data[2]
        self.student_pos = db_data[3]
        self.employee_cc = db_data[4]
        self.employee_pos = db_data[5]
        self.total = db_data[6]

class FSUTestingReport:
    def __init__(self, db_data: Tuple):
        self.id = db_data[0]
        self.start = datetime.fromtimestamp(db_data[1])
        self.end = datetime.fromtimestamp(db_data[2])
        self.test_count = db_data[3]
        self.student_pos = db_data[4]
        self.employee_pos = db_data[5]
        self.total_pos = db_data[6]
        self.pos_rate = db_data[7]

class FSUReportedCases:
    def __init__(self, db_data: Tuple):
        self.id = db_data[0]
        self.timestamp = datetime.fromtimestamp(db_data[1])
        self.count = db_data[2]

class FSUPopulation:
    def __init__(self, db_data: Tuple):
        self.id = db_data[0]
        self.year = db_data[1]
        self.students = db_data[2]
        self.employees = db_data[3]
        self.total = db_data[4]

class LeonMetrics:
    def __init__(self, db_data: Tuple):
        self.id = db_data[0]
        self.timestamp = datetime.fromtimestamp(db_data[1])
        self.pos_test_ratio = db_data[2]
        self.cases_per_capita = db_data[3]
        self.r_naught = db_data[4]
        self.r_naught_ci90 = db_data[5]
        self.vac_ratio = db_data[6]

class LeonActuals:
    def __init__(self, db_data: Tuple):
        self.id = db_data[0]
        self.timestamp = datetime.fromtimestamp(db_data[1])
        self.total_cases = db_data[2]
        self.total_deaths = db_data[3]
        self.new_cases = db_data[4]
        self.new_deaths = db_data[5]
        self.vac_count = db_data[6]