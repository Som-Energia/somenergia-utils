# Change log

## somutils 1.8.0 2022-04-07

- `testutils.temp_path`: context manager to get a self destructed temporary directory as Path

## somutils 1.7.3 2022-02-08

- First changelog entry
- Fixes Python 2.7 compat (conditionally version constrained dependencies)
- isodates fixed missimplementations
  - isodates.daterange(first_date, last_date)
  - isodates.localisodate (iso date string to datetime at local 00:00)
  - isodates.utcisodate (iso date string to datetime at UTC 00:00)
  - isodates.naiveisodate (iso date string to datetime at naive 00:00)
  - isodates.isodatetime (parses iso datetime keeping it native or timezoned)
  - isodates.localisodatetime (reinterprets naive, converts timezoned)
  - isodates.utcisodatetime (reinterprets naive, converts timezoned)
  - removed isodates.naiveisodatetime 
- Importable sql2csv
- pytest as test runner
- Continuous integration with github actions


