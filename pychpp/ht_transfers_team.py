from pychpp import ht_model
from pychpp import ht_xml, ht_datetime
import datetime as dt


class HTTransfersTeam(ht_model.HTModel):
    """
    Transfer list details for a team
    """

    _SOURCE_FILE = "transfersteam"
    _SOURCE_FILE_VERSION = "1.2"

    _URL_PATH = "/Club/Transfers/transfersTeam.aspx?teamId="

    _ht_attributes = [
        ("ht_id", "Team/TeamID", ht_xml.HTXml.ht_int),
        ("name", "Team/TeamName", ht_xml.HTXml.ht_str),
        ("activated_date", "Team/ActivatedDate",
         ht_xml.HTXml.opt_ht_datetime_from_text),
        ("total_sum_of_buys", "Stats/TotalSumOfBuys", ht_xml.HTXml.ht_int),
        ("total_sum_of_sales", "Stats/TotalSumOfSales", ht_xml.HTXml.ht_int),
        ("number_of_buys", "Stats/NumberOfBuys", ht_xml.HTXml.ht_int),
        ("number_of_sales", "Stats/NumberOfSales", ht_xml.HTXml.ht_int),
        ("page_index", "Transfers/PageIndex", ht_xml.HTXml.ht_int),
        ("pages", "Transfers/Pages", ht_xml.HTXml.ht_int),
        ("start_date", "Transfers/StartDate",
         ht_xml.HTXml.opt_ht_datetime_from_text),
        ("end_date", "Transfers/EndDate",
         ht_xml.HTXml.opt_ht_datetime_from_text),
    ]

    def __init__(self, ht_id=None, page_index=None, **kwargs):
        """
        Initialization of a HTTransferList instance

        :param ht_id: Hattrick ID of requested team
        :type ht_id: int
        :param page_index: What page in the list to retrieve
        :type pageIndex: int or str
        :key chpp: CHPP instance of connected user
        :type chpp: chpp.CHPP
        """
        self._REQUEST_ARGS = dict()
        self._REQUEST_ARGS["teamID"] = str(ht_id) if ht_id is not None else ""

        # page_index can be an integer (index) or a string equal to "all"
        # if integer, fetch corresponding page
        # if equal to "all", fetch all transfers
        if isinstance(page_index, int) or page_index is None:

            self._REQUEST_ARGS["pageIndex"] = (str(page_index)
                                               if page_index is not None
                                               else "")

            super().__init__(**kwargs)

            self.transfer_list = [
                HTTransfersTeamItem(chpp=self._chpp, data=data)
                for data in self._data.findall("Transfers/Transfer")]

        elif page_index == "all":

            self._REQUEST_ARGS["pageIndex"] = "1"
            super().__init__(**kwargs)

            self.transfer_list = [
                HTTransfersTeamItem(chpp=self._chpp, data=data)
                for data in self._data.findall("Transfers/Transfer")]

            # Store end_date of first page to restore it
            # once all transfers are fetch
            end_date = self.end_date
            pages = self.pages

            # Loop to fetch every available page
            for i in range(2, pages + 1):
                self._REQUEST_ARGS["pageIndex"] = str(i)
                super().__init__(**kwargs)
                self.transfer_list = self.transfer_list + [
                    HTTransfersTeamItem(chpp=self._chpp, data=data)
                    for data in self._data.findall("Transfers/Transfer")
                ]

            # Adapt self.page to show it represents all pages
            # and restore end_date
            self.page_index = page_index
            self.end_date = end_date

        else:
            raise ValueError("page_index must be an integer "
                             "or a string equal to 'all'")

    def __repr__(self):
        return f"<{self.__class__.__name__} object : " \
               f"{self.name} ({self.ht_id})>"


class HTTransfersTeamItem(ht_model.HTModel):
    """
    Object returned by HTTransferList.search method
    """

    _ht_attributes = [("ht_id", "TransferID", ht_xml.HTXml.ht_int,),
                      ("deadline", "Deadline",
                       ht_xml.HTXml.opt_ht_datetime_from_text,),
                      ("transfer_type", "TransferType", ht_xml.HTXml.ht_str,),
                      ("price", "Price", ht_xml.HTXml.ht_int,),
                      ("player_id", "Player/PlayerID", ht_xml.HTXml.ht_int,),
                      ("player_name", "Player/PlayerName",
                       ht_xml.HTXml.ht_str,),
                      ("tsi", "Player/TSI", ht_xml.HTXml.ht_int,),
                      ("buyer_team_id", "Buyer/BuyerTeamID",
                       ht_xml.HTXml.ht_int,),
                      ("buyer_team_name", "Buyer/BuyerTeamName",
                       ht_xml.HTXml.ht_str,),
                      ("seller_team_id", "Seller/SellerTeamID",
                       ht_xml.HTXml.ht_int,),
                      ("seller_team_name", "Seller/SellerTeamName",
                       ht_xml.HTXml.ht_str,),
                      ]

    def __lt__(self, other):
        if (isinstance(other, dt.datetime)
                or isinstance(other, ht_datetime.HTDatetime)):
            return self.deadline < other
        elif isinstance(other, HTTransfersTeamItem):
            return self.deadline < other.deadline
        else:
            raise TypeError(
                f"unsupported operand type(s) for -: "
                f"'{self.__class__.__name__}' "
                f"and '{other.__class__.__name__}'"
            )

    def __le__(self, other):
        if (isinstance(other, dt.datetime)
                or isinstance(other, ht_datetime.HTDatetime)):
            return self.deadline <= other
        elif isinstance(other, HTTransfersTeamItem):
            return self.deadline <= other.deadline
        else:
            raise TypeError(
                f"unsupported operand type(s) for -: "
                f"'{self.__class__.__name__}' "
                f"and '{other.__class__.__name__}'"
            )

    def __gt__(self, other):
        if (isinstance(other, dt.datetime)
                or isinstance(other, ht_datetime.HTDatetime)):
            return self.deadline > other
        elif isinstance(other, HTTransfersTeamItem):
            return self.deadline > other.deadline
        else:
            raise TypeError(
                f"unsupported operand type(s) for -: "
                f"'{self.__class__.__name__}' "
                f"and '{other.__class__.__name__}'"
            )

    def __ge__(self, other):
        if (isinstance(other, dt.datetime)
                or isinstance(other, ht_datetime.HTDatetime)):
            return self.deadline >= other
        elif isinstance(other, HTTransfersTeamItem):
            return self.deadline >= other.deadline
        else:
            raise TypeError(
                f"unsupported operand type(s) for -: "
                f"'{self.__class__.__name__}' "
                f"and '{other.__class__.__name__}'"
            )

    def __repr__(self):
        return f'<{self.__class__.__name__} object : ' \
               f'{self.deadline} ' \
               f'{self.transfer_type} - {self.player_name} ({self.player_id})>'
