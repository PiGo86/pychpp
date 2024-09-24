from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pychpp.chpp import CHPP


class HTTransferHistory:

    def __init__(self, chpp: 'CHPP' = None, team_id: int = None,
                 page: int = None, all_transfers: bool = False, **kwargs):

        self._chpp = chpp
        self.transfers = []
        self.stats, self.start_date, self.end_date = None, None, None

        if all_transfers is True:
            xml_transfers = self._chpp.xml_transfers_team(
                team_id=team_id,
                page_index=1,
                **kwargs,
            )
            self.transfers = xml_transfers.transfers.transfer_items
            self.stats = xml_transfers.stats
            self.start_date = xml_transfers.transfers.start_date
            self.end_date = xml_transfers.transfers.end_date

            total_pages = xml_transfers.transfers.pages
            for page in range(2, total_pages + 1):
                xml_transfers = self._chpp.xml_transfers_team(
                    team_id=team_id,
                    page_index=page,
                    **kwargs,
                )

                self.transfers += xml_transfers.transfers.transfer_items

                self.start_date = (xml_transfers.transfers.start_date
                                   if xml_transfers.transfers.start_date < self.start_date
                                   else self.start_date
                                   )
                self.end_date = (xml_transfers.transfers.end_date
                                 if xml_transfers.transfers.end_date > self.end_date
                                 else self.end_date
                                 )

        else:
            xml_transfers = self._chpp.xml_transfers_team(
                team_id=team_id,
                page_index=page,
                **kwargs,
            )
            self.transfers = xml_transfers.transfers.transfer_items
            self.stats = xml_transfers.stats
            self.start_date = xml_transfers.transfers.start_date
            self.end_date = xml_transfers.transfers.end_date

    def __getitem__(self, item):
        return self.transfers[item]

    def __len__(self):
        return len(self.transfers)
