from urllib.parse import urlencode

from pychpp.models.ht_model import HTModel


class CustomModel(HTModel):
    """
    Base class for custom models
    """

    _BASE_URL: str = "https://www.hattrick.org/goto.ashx?path="

    @property
    def url(self):

        if self._url:
            return self._url

        elif self.URL_PATH is not None:
            args = {
                ivar.param: self._requests_args.get(ivar.param, getattr(self, str(ivar.fill_with), None))
                for ivar in self._ht_init_vars.values()
                if 'id' in ivar.param.lower()
                   and self._requests_args.get(ivar.param, getattr(self, str(ivar.fill_with), None)) is not None
            }
            params = urlencode(args)
            if params:
                self._url = f"{self._BASE_URL}{self.URL_PATH}?{params}"
            else:
                self._url = f"{self._BASE_URL}{self.URL_PATH}"

            return self._url

        else:
            return None