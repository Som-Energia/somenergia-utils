import unittest
from .erptree import erptree
from yamlns import ns

class ModelMock:
    """Emulates an erppeek model object"""

    def __init__(self, instances):
        self.instances = dict(
            (x['id'], x)
            for x in instances
        )

    def read(self, ids, attribs=None):
        if type(ids) in (list, tuple):
            return [
                self.read(id, attribs) for id in ids
            ]
        return self.instances[ids]


class ErpTree_Test(unittest.TestCase):
    from yamlns.testutils import assertNsEqual

    modelPerson = ModelMock([
        dict(
            id=12,
            name='Palotes, Perico',
            username='ppalotes',
            address=(1,'13 Rue Percebe')
        ),
        dict(
            id=13,
            name='Inchains, Alice',
            username='alice',
            address=(2, '32, Road Trip, Seattle')
        ),
    ])

    modelAddress = ModelMock([
        dict(
            id=1,
            name='13 Rue Percebe',
        ),
        dict(
            id=2,
            name="32, Road Trip, Seattle",
        ),
    ])

    modelGroup = ModelMock([
        dict(
            id=100,
            name="Grunge groups",
            members=[12,13],
        ),
    ])


    def test_singleId(self):
        result = erptree(12, self.modelPerson)
        self.assertNsEqual(ns(result=result), """
          result:
            id: 12
            name: Palotes, Perico
            username: ppalotes
            address:
            - 1
            - 13 Rue Percebe
        """)

    def test_multipleId(self):
        result = erptree([12,13], self.modelPerson)
        self.assertNsEqual(ns(result=result), """
          result:
          - id: 12
            name: Palotes, Perico
            username: ppalotes
            address:
            - 1
            - 13 Rue Percebe
          - id: 13
            name: Inchains, Alice
            username: alice
            address:
            - 2
            - 32, Road Trip, Seattle
        """)

    def test_singleId_annonymize(self):
        result = erptree(12, self.modelPerson,
            anonymize='name',
        )
        self.assertNsEqual(ns(result=result), """
          result:
            id: 12
            name: Pal...ico  # this is annonimized
            username: ppalotes
            address:
            - 1
            - 13 Rue Percebe
        """)

    def test_singleId_remove(self):
        result = erptree(12, self.modelPerson,
            remove='id',
        )
        self.assertNsEqual(ns(result=result), """
          result:
            # id: 12         # This is removed
            name: Palotes, Perico
            username: ppalotes
            address:
            - 1
            - 13 Rue Percebe
        """)

    def test_singleId_pickName(self):
        result = erptree(12, self.modelPerson,
            pickName='address',
        )
        self.assertNsEqual(ns(result=result), """
          result:
            id: 12
            name: Palotes, Perico
            username: ppalotes
            address: 13 Rue Percebe    # name picked
        """)

    def test_singleId_pickId(self):
        result = erptree(12, self.modelPerson,
            pickId='address',
        )
        self.assertNsEqual(ns(result=result), """
          result:
            id: 12
            name: Palotes, Perico
            username: ppalotes
            address: 1     # id picked
        """)

    def test_singleId_expand_one2one(self):
        result = erptree(12, self.modelPerson,
            expand=dict(
                address=self.modelAddress,
            ),
        )
        self.assertNsEqual(ns(result=result), """
          result:
            id: 12
            name: Palotes, Perico
            username: ppalotes
            address:
              id: 1
              name: 13 Rue Percebe
        """)

    def test_singleId_expand_one2many(self):
        result = erptree(100, self.modelGroup,
            expand=dict(
                members=self.modelPerson,
            ),
        )
        self.assertNsEqual(ns(result=result), """
          result:
            id: 100
            name: Grunge groups
            members:
            - id: 12
              name: Palotes, Perico
              username: ppalotes
              address:
              - 1
              - 13 Rue Percebe
            - id: 13
              name: Inchains, Alice
              username: alice
              address:
              - 2
              - 32, Road Trip, Seattle
        """)

    def test_singleId_expand_applyExpanded(self):
        result = erptree(100, self.modelGroup,
            expand={
                'members': self.modelPerson,
                'members.address': self.modelAddress,
            },
            remove=[
                'members.address.id',
            ],
            anonymize=[
                'members.address.name',
            ],
        )
        self.assertNsEqual(ns(result=result), """
          result:
            id: 100
            name: Grunge groups
            members:
            - id: 12
              name: Palotes, Perico
              username: ppalotes
              address:           # expanded
                # id: 1          # removed
                name: 13 ...ebe  # anonymized
            - id: 13
              name: Inchains, Alice
              username: alice
              address:           # expanded
                # id: 2          # removed
                name: 32,...tle  # anonymized
        """)

# TODO: only in plain
# TODO: only in inner
# TODO: only in one2many
# TODO: only with expand
# TODO: only with expand in inner
# TODO: only with expand in one2many


