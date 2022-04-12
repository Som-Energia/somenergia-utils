# Change log

## somutils 1.8.1 2022-04-12

- Fix: sql2csv was unable to run
- Some traces removed

## somutils 1.8.0 2022-04-11

- new utilities:
  - `tsv` module: quick serialization of dict objects as TSV files (`tsvread`/`tsvwrite`) 
  - `testutils.temp_path()`: context manager to get a self destructed temporary directory as Path
  - `testutils.working_dir(path)`: context manager to run code with a changed working directory
  - `testutils.sandbox_dir()`: context manager to run code with a self-destructed temporary directory as the working dir 
  - `dbutils.runsql`: running parametrized sql files
  - `dbutils.runsql_cached`: like runsql but using a tsv file as cache to avoid repeated execution
- `sql2csv` deconstructed on the previous functions
- `sql2csv` has a new `-o` option to dump to a file
- Test coverage from 23% to 80%

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


