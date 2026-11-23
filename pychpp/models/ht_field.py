"""Dataclasses describing how model attributes map to the xml data."""

from dataclasses import dataclass, field
from typing import Type

from pychpp.models import ht_model


@dataclass
class HTBaseField:
    """Base dataclass for the field descriptors."""
    pass


@dataclass
class HTField(HTBaseField):
    """Descriptor mapping a model attribute to an xml path.

    Args:
        path: Xml path of the data.
        version: Version constraint of the file in which the path exists.
        items: Tag of the items when the field maps to a list.
        attrib: Name of the xml attribute to read instead of the text.
        xml_prefix: Prefix added to the path.
        suppl_attrs: Additional attributes used to build the path.

    """
    path: str
    version: str = None
    items: str = None
    attrib: str = None
    xml_prefix: str = None
    suppl_attrs: dict = field(default_factory=dict)


@dataclass
class HTAliasField(HTBaseField):
    """Descriptor mapping a model attribute to another attribute.

    Args:
        target: Name of the target attribute.

    """
    target: str


@dataclass
class HTProxyField(HTBaseField):
    """Descriptor mapping a model attribute to a field of another model class.

    Args:
        cls: Target model class.
        attr_name: Name of the target attribute (defaults to the attribute name).
        xml_prefix: Prefix added to the resolved path.
        suppl_attrs: Additional attributes used to build the path.

    """
    cls: Type['ht_model.HTModel']
    attr_name: str = None
    xml_prefix: str = ''
    suppl_attrs: dict = field(default_factory=dict)
