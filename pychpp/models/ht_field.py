from dataclasses import dataclass
from typing import Type, TypeVar

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



@dataclass
class HTAliasField(HTBaseField):
    target: str


@dataclass
class HTProxyField(HTBaseField):
    cls: Type['ht_model.HTModel']
    attr_name: str
    xml_prefix: str = ''