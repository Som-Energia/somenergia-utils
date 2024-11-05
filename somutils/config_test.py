from __future__ import unicode_literals
import unittest
from .testutils import sandbox_dir
from .config import load_py_config

class Config_Test(unittest.TestCase):

    from .testutils import assertNsEqual

    def test__load_py_config(self):
        with sandbox_dir() as baseurl:
            config_file = baseurl/'myconfig.py'
            config_file.write_text(
                "_ignored = 'value'\n"
                "param = 3\n"
                "param2 = 3 + 3\n"
            )

            config = load_py_config(config_file)

            self.assertNsEqual(config, """
                param: 3
                param2: 6
            """)

