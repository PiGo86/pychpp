class HTVersion:

    def __init__(self, version: str):
        self.as_string = version
        self.major = int(version.split('.')[0])
        self.minor = int(version.split('.')[1])

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            if self.major == other.major:
                return self.minor < other.minor
            else:
                return self.major < other.major
        else:
            return TypeError(f"can not compare {other.__class__.__name__}"
                             f" instance with HTVersion instance")

    def __le__(self, other):
        if isinstance(other, self.__class__):
            if self.major == other.major:
                return self.minor <= other.minor
            else:
                return self.major <= other.major
        else:
            return TypeError(f"can not compare {other.__class__.__name__}"
                             f" instance with HTVersion instance")

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.major, self.minor) == (other.major, other.minor)
        else:
            return TypeError(f"can not compare {other.__class__.__name__}"
                             f" instance with HTVersion instance")


class HTVersionConstraint:

    def __init__(self, version_constraint: str):

        if version_constraint[0] == '=':
            self.constraint = 'eq'

        elif version_constraint[0:2] == '<=':
            self.constraint = 'le'

        elif version_constraint[0:2] == '>=':
            self.constraint = 'ge'

        elif version_constraint[0] == '<':
            self.constraint = 'lt'

        elif version_constraint[0] == '>':
            self.constraint = 'gt'

        else:
            raise ValueError("Unknown version constraint")

        if self.constraint in ('le', 'ge'):
            self.version = HTVersion(version_constraint[2:])
        else:
            self.version = HTVersion(version_constraint[1:])

    def is_valid(self, ht_version: HTVersion):

        if self.constraint == 'eq':
            return ht_version == self.version

        elif self.constraint == 'gt':
            return ht_version > self.version

        elif self.constraint == 'ge':
            return ht_version >= self.version

        elif self.constraint == 'lt':
            return ht_version < self.version

        elif self.constraint == 'le':
            return ht_version <= self.version
