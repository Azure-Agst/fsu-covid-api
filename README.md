# FSU Covid API

API written in Python/Flask that serves scraped Covid data from a local sqlite3 database.

Obvi it only serves FSU/Leon County data, as that's where the university is located.

-----

## Running Locally

The following instructions are written for WSL. You'll need a copy of the database to get started, as it's not auto-generated yet.

1. Clone the repo
2. `python3 -m venv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `flask run --host=[ip]` (Replace `[ip]` with WSL VM's IP)
6. Profit?

-----

## Authentication

Authentication is pretty simple, using only a single query parameter. Just put your API key inside a query parameter, `apikey`, then make a request.

To get an API key, add a user row into `users.data`. Eventually this will have an endpoint to make things nicer.

-----

## Endpoints

There are many in development, but here are a few big ones.

### GET `/all.json`

- Returns all FSU and Leon County Covid data.

### GET `/fsu.json`

- Returns all FSU Covid data.

### GET `/leon.json`

- Returns all Leon County Covid data.

-----

## Data Models

### `fsu.reported_cases`

- `last_updated` - The date the following data corresponds with, in YYYY-MM-DD format.
- `new_cases` - The number of daily new FSU-affiliated Covid-19 cases reported by the university and its partners.
- `total` - Total number of cases reported by the university since Aug 1, 2021.

### `fsu.estimates`

- `population`
  - `year` - The year the following data corresponds with.
  - `students` - The number of students enrolled at FSU that year.
  - `employees` - The number of employees working at FSU that year.
  - `total` - The total number of students and employees that year.
- `students`
  - `positive` - The number of students that are currently estimated by the university to be in quarantine, due to a positive Covid-19 test.
  - `close_contacts` - The number of students that are currently estimated by the university to be in quarantine, due to recently being in close contact with someone who tested positive for Covid-19.
- `employees`
  - `positive` - The number of employees that are currently estimated by the university to be in quarantine, due to a positive Covid-19 test.
  - `close_contacts` - The number of employees that are currently estimated by the university to be in quarantine, due to recently being in close contact with someone who tested positive for Covid-19.
- `total_quarantined` - The total number of people the university expects to be in quarantine.
- `last_updated` - The date the above data corresponds with, in YYYY-MM-DD format.

### `fsu.testing`

- `start` - The beginning of the date range associated with the below data.
- `end` - The end of the date range associated with the below data.
- `total_tests` - The total number of tests administered by FSU UHS within the date range.
- `students`
  - `positive` - The number of student positive tests reported within the date range.
- `employees`
  - `positive` - The number of employee positive tests reported within the date range.
- `total_positives` - The total number of positive tests reported within the date range.
- `positivity_rate` - The number calculated from taking the number of positive tests, and dividing by total test count.

### `leon.metrics`

- `last_updated` - The date the below data corresponds with, in YYYY-MM-DD format.
- `positivity_rate` - The number calculated from taking the number of positive tests, and dividing by total test count.
- `cases_per_100k` - The number of people expected to be positive within a population of 100k people.
- `r_naught` - R-Naught, or the estimated number of infections arising from a typical case.
- `r_naught_ci90` - 90th percentile confidence interval upper endpoint of the infection rate.
- `vaccination_ratio` - Ratio of vaccinated people to unvaccinated people within Leon County.

### `leon.actuals`

- `last_updated` - The date the below data corresponds with, in YYYY-MM-DD format.
- `total_cases` - Total number of covid cases confirmed within Leon County.
- `total_deaths` - Total number of covid-related deaths confirmed within Leon County.
- `new_cases` - Total number of new covid cases reported on this date.
- `new_deaths` - Total number of new covid-related deaths reported on this date.
- `vac_count` - The number of vaccinated citizens within Leon County.

### `annotations`

- `corresponding_category_name` (i.e. `leon.actuals`, `fsu.estimates`)
  - `index`
    - `name` - The name of the source
    - `url` - The URL where the data was obtained from
    - `notes` - Notes, usually about how the data was obtained

-----

## Contributing

It's welcome! But I don't have any guidelines set just yet... Soon!

-----

*Developed/Maintained by [Azure-Agst](https://azureagst.dev) :)*
