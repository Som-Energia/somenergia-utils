import unittest
from yamlns import ns
from .testutils import sandbox_dir, Path
from .dbutils import runsql, MissingParameter
import os

def pgconfig_from_environ():
    environs = dict(
        host='PGHOST',
        user='PGUSER',
        password='PGPASSWORD',
        port='PGPORT',
        database='PGDATABASE',
        passfile='PGPASSFILE',
        hostaddr='PGHOSTADDR',
    )
    config = dict(
        (param, value)
        for param, value in (
            (param, os.environ.get(var, None))
            for param, var in environs.items()
        )
        if value is not None
    )
    return config or dict(database='postgres')

@unittest.skipIf(not pgconfig_from_environ(),
    "Please specify PGxxx variables to enable those tests"
)
class DBUtils_Test(unittest.TestCase):

    from yamlns.testutils import assertNsEqual

    def write(self, file, content):
        Path(file).write_text(content, encoding='utf8')

    def test_runsql_helloworld(self):
        with sandbox_dir() as sandbox:
            config = pgconfig_from_environ()

            self.write('hello.sql',
                "SELECT 'world' as hello"
            )

            result = runsql('hello.sql', config=config)

            self.assertNsEqual(ns(data=list(result)), """\
              data:
              - hello: world
            """)

    def test_runsql_configfile(self):
        with sandbox_dir() as sandbox:
            self.write('myconfig.py',
                "psycopg = {!r}".format(pgconfig_from_environ())
            )
            self.write('hello.sql',
                "SELECT 'world' as hello"
            )

            result = runsql('hello.sql', config='myconfig.py')

            self.assertNsEqual(ns(data=list(result)), """\
              data:
              - hello: world
            """)

    @unittest.skip("Python path must be altered")
    def test_runsql_default_dbconfig(self):
        with sandbox_dir() as sandbox:
            self.write('dbconfig.py',
                "psycopg = {!r}".format(pgconfig_from_environ())
            )
            self.write('hello.sql',
                "SELECT 'world' as hello"
            )

            result = runsql('hello.sql')

            self.assertNsEqual(ns(data=list(result)), """\
              data:
              - hello: world
            """)

    def test_runsql_parametrized(self):
        with sandbox_dir() as sandbox:
            config = pgconfig_from_environ()
            self.write('hello.sql',
                "SELECT %(name)s as hello"
            )

            result = runsql('hello.sql', config=config, name='Perico')

            self.assertNsEqual(ns(data=list(result)), """\
              data:
              - hello: Perico
            """)

    def test_runsql_parametrized_list_asArray(self):
        with sandbox_dir() as sandbox:
            config = pgconfig_from_environ()
            self.write('hello.sql',
                "SELECT %(ids)s as hello"
            )

            result = runsql('hello.sql', config=config, ids=[1,2,3])

            self.assertNsEqual(ns(data=list(result)), """\
              data:
              - hello:
                - 1
                - 2
                - 3
            """)

    def test_runsql_parametrized_tuple_asSet(self):
        with sandbox_dir() as sandbox:
            config = pgconfig_from_environ()
            self.write('hello.sql',
                "SELECT 2 in %(ids)s as hello"
            )
            result = runsql('hello.sql', config=config, ids=(1,2,3))

            self.assertNsEqual(ns(data=list(result)), """\
              data:
              - hello: true
            """)

    def test_runsql_missingParameter(self):
        with sandbox_dir() as sandbox:
            config = pgconfig_from_environ()
            self.write('hello.sql',
                "SELECT %(forgottenParameter)s as hello"
            )

            with self.assertRaises(MissingParameter) as ctx:
                result = runsql('hello.sql', config=config)
                list(result) # fetch to force load

            self.assertEquals(format(ctx.exception),
                "forgottenParameter"
            )

    def test_runsql_multirow(self):
        with sandbox_dir() as sandbox:
            config = pgconfig_from_environ()
            self.write('hello.sql', """\
                SELECT * FROM (VALUES
                    ('alice', 34),
                    ('bob', 29),
                    ('cynthia', 25))
                AS mytable(name, points)
            """)

            result = runsql('hello.sql', config=config)

            self.assertNsEqual(ns(data=list(result)), """\
              data:
              - name: alice
                points: 34
              - name: bob
                points: 29
              - name: cynthia
                points: 25
            """)


