# Change log

## somutils 1.10.0 2024-11-05

- Back support for python from 2.7 to 3.12
- New somutils.config module to load python configurations in a portable way

## somutils 1.9.1 2023-11-20

- Fix requirement 'google-auth' not working for py2

## somutils 1.9.0 2023-09-11

- Added testutils.enterContext, a polyfill for
  unittest.TestCase.enterContext introduced in Python 3.11.
  Eases the use of context handlers in setUp.

## somutils 1.8.5 2022-06-15

- py2: requests dropped py2

## somutils 1.8.4 2022-06-15

- Documentation updated
- py2: certifi dropped py2

## somutils 1.8.3 2022-04-13

- py2 tests fixed (mutating looping dict)

## somutils 1.8.2 2022-04-13

- `pgconfig_from_environ` added to use standard pqsl env vars as means of configuration
- `pgconfig_from_environ` custom var prefixes to enable multiple databases

## somutils 1.8.1 2022-04-12

- Fix: sql2csv refered to an unexisting variable
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


