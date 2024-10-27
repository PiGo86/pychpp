from dataclasses import dataclass, field
from typing import Type

from pychpp.models import ht_model


@dataclass
class HTBaseField:
    pass


@dataclass
class HTField(HTBaseField):
    path: str
    version: str = None
    items: str = None
    attrib: str = None
    xml_prefix: str = None
    suppl_attrs: dict = field(default_factory=dict)


@dataclass
class HTAliasField(HTBaseField):
    target: str


@dataclass
class HTProxyField(HTBaseField):
    cls: Type['ht_model.HTModel']
    attr_name: str = None
    xml_prefix: str = ''
    suppl_attrs: dict = field(default_factory=dict)
