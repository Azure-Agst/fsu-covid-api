BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "fsu.testing" (
	"id"	INTEGER NOT NULL UNIQUE,
	"start"	INTEGER,
	"end"	INTEGER,
	"test_count"	INTEGER,
	"pos_student"	INTEGER,
	"pos_employee"	INTEGER,
	"pos_total"	INTEGER,
	"pos_rate"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "fsu.estimates" (
	"id"	INTEGER NOT NULL UNIQUE,
	"timestamp"	INTEGER,
	"student_ccs"	INTEGER,
	"student_pos"	INTEGER,
	"employee_ccs"	INTEGER,
	"employee_pos"	INTEGER,
	"total"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "users.data" (
	"id"	INTEGER NOT NULL UNIQUE,
	"email"	TEXT,
	"apikey"	TEXT,
	"ratelimit"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "annotations" (
	"id"	INTEGER NOT NULL UNIQUE,
	"src_table"	TEXT,
	"name"	TEXT,
	"url"	TEXT,
	"notes"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "fsu.reported_cases" (
	"id"	INTEGER NOT NULL UNIQUE,
	"timestamp"	INTEGER,
	"count"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "fsu.population" (
	"id"	INTEGER NOT NULL UNIQUE,
	"year"	INTEGER,
	"students"	INTEGER,
	"employees"	INTEGER,
	"total"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "leon.population" (
	"id"	INTEGER NOT NULL UNIQUE,
	"year"	INTEGER,
	"population"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "leon.metrics" (
	"id"	INTEGER NOT NULL UNIQUE,
	"timestamp"	INTEGER,
	"pos_test_ratio"	REAL,
	"cases_per_capita"	REAL,
	"r_naught"	REAL,
	"r_naught_ci90"	REAL,
	"vac_ratio"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "leon.actuals" (
	"id"	INTEGER NOT NULL UNIQUE,
	"timestamp"	INTEGER,
	"total_cases"	INTEGER,
	"total_deaths"	INTEGER,
	"new_cases"	INTEGER,
	"new_deaths"	INTEGER,
	"vac_count"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "users.canaries" (
	"id"	INTEGER NOT NULL UNIQUE,
	"timestamp"	INTEGER,
	"ip"	TEXT,
	"canary"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "users.logs" (
	"id"	INTEGER NOT NULL UNIQUE,
	"timestamp"	INTEGER,
	"user_id"	INTEGER,
	"canary"	INTEGER,
	"ip"	INTEGER,
	"query"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
COMMIT;
