from copy import copy
from typing import Optional, Type, Dict, Any, List
import xml.etree.ElementTree as ElementTree
from datetime import datetime
from typing import get_type_hints, get_origin, Union, get_args
from urllib.parse import urlencode

import pychpp.chpp as _chpp
from pychpp.ht_xml import HTXml
from pychpp.models.ht_field import HTBaseField, HTField, HTAliasField, HTProxyField
from pychpp.models.ht_init_var import HTInitVar


class MetaHTModel(type):
    """
    Metaclass used for registering ht_init_vars and ht_fields
    declared in current class and its ancestors
    """
    def __new__(cls, name, bases, dict_):

        dict_['_ht_fields'] = dict()
        dict_['_ht_init_vars'] = dict()

        for b in bases:
            if issubclass(b, HTModel):
                dict_['_ht_fields'].update(b.__dict__['_ht_fields'])
                dict_['_ht_init_vars'].update(b.__dict__['_ht_init_vars'])

        for attr_name, attr_value in dict_.items():
            if isinstance(attr_value, HTBaseField):
                dict_['_ht_fields'].update({attr_name: attr_value})
            if isinstance(attr_value, HTInitVar):
                dict_['_ht_init_vars'].update({attr_name: attr_value})

        return super().__new__(cls, name, bases, dict_)

class HTModel(metaclass=MetaHTModel):

    _BASE_URL: str = "https://www.hattrick.org/goto.ashx?path="

    SOURCE_FILE: List[str]
    LAST_VERSION: str
    URL_PATH: Optional[str] = None
    XML_PREFIX: str = ''
    XML_FILTER: str = ''

    _ht_fields: Dict[str, Union[HTField, HTAliasField]]
    _ht_init_vars: Dict[str, HTInitVar]

    @classmethod
    def is_optional_attrib(cls, attrib: str) -> bool:
        typehint = get_type_hints(cls).get(attrib)
        return get_origin(typehint) is Union and type(None) in get_args(typehint)

    @classmethod
    def get_type(cls, attrib: str) -> Any:
        typehint = get_type_hints(cls).get(attrib)

        _type = typehint
        if cls.is_optional_attrib(attrib):
            _type = list(*{get_args(typehint)}.difference({type(None)}))[0]

        _type = _type if get_origin(_type) is None else get_origin(_type)

        return _type

    @classmethod
    def get_item_type(cls, attrib: str) -> Any:
        if cls.get_type(attrib) is not list:
            return None

        else:
            typehint = get_type_hints(cls).get(attrib)

            if cls.is_optional_attrib(attrib):
                list_hint = list(*{get_args(typehint)}.difference({type(None)}))[0]
            else:
                list_hint = typehint

            list_arg = get_args(list_hint)

            if not list_arg or get_origin(list_arg[0]) in (Union, Optional):
                raise ValueError(f"HTModel does not support list typehint without argument, "
                                 f"nor Union or Optional arguments")

            else:
                return list_arg[0]

    def __init__(self,
                 chpp: Union['_chpp.CHPPBase', '_chpp.CHPPXml', '_chpp.CHPP'],
                 data: Optional[ElementTree.Element] = None,
                 version: Optional[str] = None,
                 xml_prefix: str = None,
                 **kwargs,
                 ):

        self._pre_init(**kwargs)

        if not isinstance(chpp, _chpp.CHPP):
            raise ValueError("chpp must be a CHPP instance")

        elif not isinstance(data, ElementTree.Element) and data is not None:
            raise ValueError("data must be an xml.etree.ElementTree.Element instance")

        elif data is None and getattr(self, 'SOURCE_FILE', None) is None:
            raise ValueError("data cannot be 'None' when class attribute 'SOURCE_FILE' is unset")

        self._chpp = chpp
        self._data = data
        self.version = version
        self.xml_prefix = xml_prefix if xml_prefix is not None else self.XML_PREFIX
        # if data is not given, fetch data on Hattrick
        if self._data is None:
            self._fetch(version, **kwargs)

        self._transform_fields()

    def _fetch(self, version, **kwargs):

        self.version = version if version is not None else self.LAST_VERSION

        self._requests_args = dict()

        for attr, ht_init_var in self._ht_init_vars.items():

            ht_init_var.value = kwargs.get(ht_init_var.init_arg, None)

            if ht_init_var.value is None and not self.is_optional_attrib(attr):
                raise ValueError(f"{ht_init_var.init_arg} argument has to be set "
                                 f"as {attr} is not optional")
            elif ht_init_var.value is None:
                ht_init_var.value = ht_init_var.default

            if ht_init_var.value is not None:
                self._requests_args[ht_init_var.param] = ht_init_var.value

            setattr(self, attr, ht_init_var.value)

        self._data = self._chpp.request(file=self.SOURCE_FILE,
                                        version=self.version,
                                        **self._requests_args,
                                        )

    def _transform_fields(self):

        # Fill attributes according to class attributes referencing a HTBaseField instance

        for field_name, field in self._ht_fields.items():

            if isinstance(field, HTProxyField):
                field: HTProxyField
                xml_path = field.xml_prefix
                target_cls = field.cls
                target_field = copy(field)

                for level in field.attr_name.split('.'):

                    typehint = get_type_hints(target_cls).get(level)
                    target_field = getattr(target_cls, level)
                    if xml_path and xml_path[-1] != '/':
                        xml_path += '/'
                    xml_path += target_field.path

                    if issubclass(typehint, HTModel):
                        target_cls = typehint

                field = target_field
                field.path = xml_path

            if isinstance(field, HTField):

                field: HTField

                field.type = self.get_type(field_name)
                field.item_type = self.get_item_type(field_name)
                field.is_optional = True if self.is_optional_attrib(field_name) else False

                xml_path = self.xml_prefix + self.XML_FILTER + field.path
                xml_node = self._data.find(xml_path)

                # instance attribute set to transformed value
                # according to type hint
                if field.type is list:

                    if xml_node is None:
                        if not field.is_optional:
                            raise ValueError(f"{self.__class__} : non optional field {field} returned 'None'")
                        else:
                            setattr(self, field_name, list())
                            continue

                    if field.item_type is str:
                        setattr(self, field_name, HTXml.ht_str_items(xml_node, field.items))
                    elif issubclass(field.item_type, HTModel):
                        item_type: Type[HTModel]
                        setattr(self,
                                field_name,
                                [field.item_type(chpp=self._chpp, data=i)
                                 for i in HTXml.iter_data_items(xml_node, field.items)])
                    else:
                        raise ValueError(f"unsupported type '{field.item_type}' for list item")

                else:

                    if xml_node is None:
                        if not field.is_optional:
                            raise ValueError(f"{self.__class__} : non optional field {field} returned 'None'")
                        else:
                            setattr(self, field_name, None)
                            continue

                    if field.type is int:
                        setattr(self, field_name, HTXml.ht_int(xml_node, attrib=field.attrib))

                    elif field.type is str:
                        setattr(self, field_name, HTXml.ht_str(xml_node, attrib=field.attrib))

                    elif field.type is float:
                        setattr(self, field_name, HTXml.ht_float(xml_node, attrib=field.attrib))

                    elif field.type is bool:
                        setattr(self, field_name, HTXml.ht_bool(xml_node, attrib=field.attrib))

                    elif field.type is datetime and self.is_optional_attrib(field_name):
                        setattr(self, field_name, HTXml.ht_datetime_from_text(xml_node, attrib=field.attrib))

                    elif field.type is datetime:
                        setattr(self, field_name, HTXml.opt_ht_datetime_from_text(xml_node, attrib=field.attrib))

                    elif issubclass(field.type, HTModel):

                        setattr(self, field_name, field.type(chpp=self._chpp,
                                                             data=xml_node,
                                                             xml_prefix=field.xml_prefix,
                                                             ))

                    else:
                        raise ValueError(f"type hint '{field.type}' no implemented")

            elif isinstance(field, HTAliasField):
                field: HTAliasField
                setattr(self, field_name, getattr(self, field.target))


    def _pre_init(self, **kwargs):
        """
        hook to make some stuff at the beginning of __init__ process

        """
        pass


    @property
    def url(self):
        if self.URL_PATH is not None:
            params = urlencode(getattr(self, '_requests_args', ''))
            if params:
                return f"{self._BASE_URL}{self.URL_PATH}?{params}"
            else:
                return f"{self._BASE_URL}{self.URL_PATH}"

    def __repr__(self):
        desc = ''

        if getattr(self, 'name', None) is not None:
            desc+= f"{getattr(self, 'name')} "
        elif getattr(self, 'login_name', None) is not None:
            desc+= f"{getattr(self, 'login_name')} "

        if getattr(self, 'ht_id', None) is not None:
            desc += f"({getattr(self, 'ht_id')})"
        elif getattr(self, 'id', None) is not None:
            desc += f"({getattr(self, 'id')})"

        desc = desc.strip()

        if desc:
            desc = f" - {desc}"

        return f"<{self.__class__.__name__} object{desc}>"
