from __future__ import unicode_literals
from yamlns import namespace as ns
from consolemsg import u
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path # Py2
import csv

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

    tsv = csv.DictReader(file, delimiter=str('\t')) # Py2 hack, str
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
                fieldnames=[u(x) for x in item.keys()], # Py2
                #fieldnames=list(item.keys()), # Py3 only
                delimiter=str('\t'), # Py2 hack, str
                lineterminator='\n',
            )
            tsv.writeheader()
        tsv.writerow(dict((k,u(v)) for k,v in item.items())) # Py2 hack
        #tsv.writerow(item) # Py3 only

