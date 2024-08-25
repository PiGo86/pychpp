from typing import Optional, Type
import xml.etree.ElementTree as ElementTree
from abc import ABC
from datetime import datetime
from typing import get_type_hints, get_origin, Union, get_args
from urllib.parse import urlencode

import pychpp.chpp as _chpp
from pychpp.ht_xml import HTXml
from pychpp.models.ht_field import HTBaseField, HTField, HTAliasField
from pychpp.models.ht_init_var import HTInitVar


class HTModel(ABC):

    _BASE_URL: str = "https://www.hattrick.org/goto.ashx?path="

    SOURCE_FILE: str
    LAST_VERSION: str
    URL_PATH: Optional[str] = None

    def __init__(self,
                 chpp: '_chpp.CHPP',
                 data: Optional[ElementTree.Element] = None,
                 version: Optional[str] = None,
                 **kwargs,
                 ):

        if not isinstance(chpp, _chpp.CHPP):
            raise ValueError("chpp must be a CHPP instance")

        elif not isinstance(data, ElementTree.Element) and data is not None:
            raise ValueError("data must be an xml.etree.ElementTree.Element instance")

        elif data is None and getattr(self, 'SOURCE_FILE', None) is None:
            raise ValueError("data has to be set as class attribute 'SOURCE_FILE' is unset")

        self._chpp = chpp
        self._data = data

        # if data is not given, fetch data on Hattrick
        if self._data is None:
            self._fetch(version, **kwargs)

        self._transform_fields()

    def _fetch(self, version, **kwargs):

        self.version = version if version is not None else self.LAST_VERSION

        self._requests_args = dict()

        for attr in (a for a in dir(self) if isinstance(getattr(self, a), HTInitVar)):
            init_var = getattr(self, attr)
            init_var.value = kwargs.get(attr, None)

            if init_var.value is None:
                init_var.value = init_var.default

            if init_var.value is not None:
                self._requests_args[init_var.param] = init_var.value

            setattr(self, attr, init_var.value)

        self._data = self._chpp.request(file=self.SOURCE_FILE,
                                        version=self.version,
                                        **self._requests_args,
                                        )

    def _transform_fields(self):

        def is_optional(x: Type) -> bool:
            return get_origin(x) is Union and type(None) in get_args(x)

        # Fill attributes according to class attributes referencing a HTBaseField instance
        for attr in (a for a in self.__class__.__dict__.keys() if isinstance(getattr(self, a), HTBaseField)):
            field = getattr(self, attr)

            if isinstance(field, HTField):

                field: HTField
                typehint = get_type_hints(self.__class__).get(attr)

                # get attribute type hint
                # if it is optional (Union[None|...]), get the first type which is not NoneType
                if is_optional(typehint):
                    field.type = [t for t in get_args(typehint) if t is not None][0]
                else:
                    field.type = typehint

                xml_node = self._data.find(field.path)

                # instance attribute set to transformed value
                # according to type hint
                if get_origin(field.type) is list:
                    item_type = get_args(field.type)[0]

                    if item_type is str:
                        setattr(self, attr, HTXml.ht_str_items(xml_node, field.items))
                    elif issubclass(item_type, HTModel):
                        item_type: Type[HTModel]
                        setattr(self,
                                attr,
                                [item_type(chpp=self._chpp, data=i)
                                 for i in HTXml.iter_data_items(xml_node, field.items)])
                    else:
                        raise ValueError(f"unsupported type '{item_type}' for list item")

                elif field.type is int:
                    setattr(self, attr, HTXml.ht_int(xml_node, attrib=field.attrib))
                elif field.type is str:
                    setattr(self, attr, HTXml.ht_str(xml_node, attrib=field.attrib))
                elif field.type is float:
                    setattr(self, attr, HTXml.ht_float(xml_node, attrib=field.attrib))
                elif field.type is bool:
                    setattr(self, attr, HTXml.ht_bool(xml_node, attrib=field.attrib))
                elif field.type is datetime and is_optional(typehint):
                    setattr(self, attr, HTXml.ht_datetime_from_text(xml_node, attrib=field.attrib))
                elif field.type is datetime:
                    setattr(self, attr, HTXml.opt_ht_datetime_from_text(xml_node, attrib=field.attrib))
                elif issubclass(field.type, HTModel):
                    setattr(self, attr, field.type(chpp=self._chpp, data=xml_node))
                else:
                    raise ValueError(f"type hint '{field.type}' no implemented")

            elif isinstance(field, HTAliasField):

                field: HTAliasField
                setattr(self, attr, getattr(self, field.target))


    @property
    def url(self):
        if self.URL_PATH is not None:
            params = urlencode(getattr(self, '_requests_args', ''))
            if params:
                return f"{self._BASE_URL}{self.URL_PATH}?{params}"
            else:
                return f"{self._BASE_URL}{self.URL_PATH}"

    def __repr__(self):
        return f"<{self.__class__.__name__} object>"
