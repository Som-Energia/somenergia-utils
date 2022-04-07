from yamlns import namespace as ns
from consolemsg import step, fail
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path # Py2
import csv

def step(**args): pass

def fetchNs(cursor):
	"""
		Wraps a database cursor so that instead of providing data
		as arrays, it provides objects with attributes named
		as the query column names.
	"""

	fields = [column.name for column in cursor.description]
	for row in cursor:
		yield ns(zip(fields, row))

def nsList(cursor) :
	"""
		Given a database cursor, returns a list of objects with the fields
		as attributes for every returned row.
		Use fetchNs for a more optimal usage.
	"""
	return [e for e in fetchNs(cursor) ]

def csvTable(cursor) :
	"""
		Returns retrieved rows as a tab separated values csv with proper headers.
	"""
	fields = [column.name for column in cursor.description]
	return '\n'.join('\t'.join(str(x) for x in line) for line in ([fields] + cursor.fetchall()) )

def tsvread(file):
    """
    Provides ns objects (dict-like) from the rows of a TSV file.
    """
    if not hasattr(file, 'read'):
        with Path(file).open() as of:
            # yield from tsvread(of) # >=Py3.3
            for item in tsvread(of): # <Py3.3
                yield item
            return

    tsv = csv.DictReader(file, delimiter='\t')
    for item in tsv:
        yield ns(item)

def tsvwrite(file, iterable):
    """
    Takes an iterable of dict like objects and dumps it as a TSV file.
    Columns are taken from the keys of the first item.
    """
    if not hasattr(file, 'write'):
        with Path(file).open('w') as outputfile:
            return tsvwrite(outputfile, iterable)

    tsv = None
    for item in iterable:
        if not tsv:
            tsv = csv.DictWriter(file,
                fieldnames=item.keys(),
                delimiter='\t',
                lineterminator='\n',
            )
            tsv.writeheader()
        tsv.writerow(item)

def runsql(sqlfile, configfile=None, **kwds):
    step(sqlfile)
    step(kwds)
    if configfile:
        import imp
        config=imp.load_source('config', configfile)
    else:
        import dbconfig as config

    step("Loading {}...".format(sqlfile))
    query = Path(sqlfile).read_text(encoding='utf8')
    import psycopg2
    step("Connecting to the database...")
    db = psycopg2.connect(**config.psycopg)

    with db.cursor() as cursor :
        try:
            cursor.execute(query, kwds)
        except KeyError as e:
            fail("Missing variable '{key}'. Specify it in the YAML file or by using the --{key} option"
                .format(key=e.args[0]))
        for item in fetchNs(cursor):
            yield item


def runsql_cached(sqlfile, cachefile=None, force=False, configfile=None, **kwds):
    """
    Like runsql but the first time is run, a tsv file with the results
    is dumped, and later executions will skip the query and take those results.
    If no 'cachefile' is provided, sqlfile with '.tsv' suffix will be used.
    Setting 'force' will force the query execution and an updated dump.
    """
    if not cachefile:
        cachefile = Path(sqlfile).with_suffix('.tsv')
    cache = Path(cachefile)

    if force or not cache.exists():
        step("regenerating {}", cache)
        tsvwrite(cache, runsql(sqlfile, configfile, **kwds))

    step("Reading cache {}", cache)
    for item in tsvread(cache):
        yield item



