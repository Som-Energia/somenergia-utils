somenergia-utils
================

This module includes different Python modules and scripts ubiquiously
used on scripts in SomEnergia cooperative but with no entity by
themselves to have their own repository.

-  ``activate_wrapper.sh``: run a command under a Python virtual
   enviroment
-  ``sql2csv.py``: script to run parametrized sql queries and get the
   result as (tab separated) csv.
-  ``dbutils.py``: module with db related functions

   -  ``fetchNs``: a generator that wraps db cursors to fetch objects
      with attributes instead of psycopg arrays
   -  ``nsList``: uses the former to build a list of such object (slower
      but maybe convinient)
   -  ``csvTable``: turns the results of a query into a tab separated
      table with proper header names

-  ``sheetfetcher.py``: convenience class to retrieve data from gdrive
   spreadshets

activate\_wrapper.sh
--------------------

You have to set an environment variable VIRTUALENV\_PATH as the folder
where the VIRTUALENV is located.

::

    usage: activate_wrapper.sh COMMAND [PARAM1 [PARAM2...]]

