from dataclasses import dataclass


class HTBaseField:
    pass

@dataclass
class HTField(HTBaseField):
    path: str
    items: str = None
    attrib: str = None


@dataclass
class HTAliasField(HTBaseField):
    target: str