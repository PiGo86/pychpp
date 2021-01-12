from pychpp import ht_model
from pychpp import ht_xml


class HTTransferDetails(ht_model.HTModel):
    """
    Transfer details for player being currently on transfer list
    """

    _ht_attributes = [("asking_price", ".//TransferDetails/AskingPrice",
                       ht_xml.HTXml.ht_int,),
                      ("deadline", ".//TransferDetails/Deadline",
                       ht_xml.HTXml.ht_datetime_from_text,),
                      ("highest_bid", ".//TransferDetails/HighestBid",
                       ht_xml.HTXml.ht_int,),
                      ("max_bid", ".//TransferDetails/MaxBid",
                       ht_xml.HTXml.ht_int,),
                      ("bidder_team_id",
                       ".//TransferDetails/BidderTeam/TeamID",
                       ht_xml.HTXml.ht_str,),
                      ("bidder_team_name",
                       ".//TransferDetails/BidderTeam/TeamName",
                       ht_xml.HTXml.ht_str,),
                      ]
