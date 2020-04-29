import xml.etree.ElementTree
from pychpp import chpp as _chpp


class HTModel:
    """
    Hattrick model class
    @DynamicAttrs
    """

    _SOURCE_FILE = str()
    _SOURCE_FILE_VERSION = str()

    _HT_ATTRIBUTES = list()

    def __init__(self, chpp, data=None):

        if not isinstance(chpp, _chpp.CHPP):
            raise ValueError("chpp must be a CHPP instance")
        elif not isinstance(data, xml.etree.ElementTree.Element) and data is not None:
            raise ValueError("data must be an xml.etree.ElementTree.Element instance")

        self._chpp = chpp
        self._data = data

        # If data is not given, fetch data on Hattrick
        if self._data is None:
            self._fetch()

        self._fill_ht_attributes()

    # def __getattribute__(self, item):
    #     if (object.__getattribute__(self, "_data") is None
    #             and item != "ht_id"
    #             and item in (a[0] for a in object.__getattribute__(self, "_HT_ATTRIBUTES"))):
    #         self._fetch()
    #         self._fill_ht_attributes()
    #     return object.__getattribute__(self, item)

    def __repr__(self):
        return f"<{self.__class__.__name__} object>"

    def _fetch(self):

        self._data = self._chpp.request(file=self._SOURCE_FILE,
                                        version=self._SOURCE_FILE_VERSION,
                                        **self._REQUEST_ARGS,
                                        )

    def _fill_ht_attributes(self):
        # Set attributes according to self._HT_ATTRIBUTES list
        for attr_tuple in self._HT_ATTRIBUTES:
            setattr(self,
                    attr_tuple[0],
                    (attr_tuple[2](self._data.find(attr_tuple[1]))
                     if self._data.find(attr_tuple[1]) is not None
                     else None),
                    )
