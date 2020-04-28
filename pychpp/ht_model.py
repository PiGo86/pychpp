from pychpp import chpp as _chpp


class HTModel:
    """
    Hattrick model class
    """

    _SOURCE_FILE = str()
    _SOURCE_FILE_VERSION = str()

    _HT_ATTRIBUTES = list()

    def __init__(self, chpp):

        if not isinstance(chpp, _chpp.CHPP):
            raise ValueError("chpp must be a CHPP instance")

        self._chpp = chpp
        self._data = None
        self._fetched = False
        self._REQUEST_ARGS = dict()

        for attr_tuple in self._HT_ATTRIBUTES:
            setattr(self, attr_tuple[0], None)

    def __getattribute__(self, item):
        if (object.__getattribute__(self, "_fetched") is False
                and item != "ht_id"
                and item in (a[0] for a in object.__getattribute__(self, "_HT_ATTRIBUTES"))):
            setattr(self, "_fetched", True)
            self._fetch()
        return object.__getattribute__(self, item)

    def _fetch(self):

        self._data = self._chpp.request(file=self._SOURCE_FILE,
                                        version=self._SOURCE_FILE_VERSION,
                                        **self._REQUEST_ARGS,
                                        )

        # Settings attributes according to self._HT_ATTRIBUTES list
        for attr_tuple in self._HT_ATTRIBUTES:
            setattr(self,
                    attr_tuple[0],
                    (attr_tuple[2](self._data.find(attr_tuple[1]))
                     if self._data.find(attr_tuple[1]) is not None
                     else None),
                    )
