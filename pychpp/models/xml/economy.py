from typing import Optional

from pychpp.models.ht_field import HTField
from pychpp.models.ht_init_var import HTInitVar
from pychpp.models.ht_model import HTModel


class RequestEconomy(HTModel):
    """
    Economy - Request arguments
    """
    SOURCE_FILE = 'economy'
    LAST_VERSION = '1.4'

    _r_team_id: Optional[int] = HTInitVar('teamId', init_arg='team_id')


class Economy(RequestEconomy):
    """
    Economy
    """
    team: 'Team' = HTField('Team')


class Team(HTModel):
    """
    Economy -> Team
    """
    id: int = HTField('TeamID')
    name: str = HTField('TeamName')
    cash: int = HTField('Cash')
    expected_cash: int = HTField('ExpectedCash')
    sponsors_popularity: Optional[int] = HTField('SponsorsPopularity')
    supporters_popularity: Optional[int] = HTField('SupportersPopularity')
    fan_club_size: int = HTField('FanClubSize')
    income_spectators: int = HTField('IncomeSpectators')
    income_sponsors: int = HTField('IncomeSponsors')
    income_sponsors_bonus: int = HTField('IncomeSponsorBonuses')
    income_financial: int = HTField('IncomeFinancial')
    income_sold_players: int = HTField('IncomeSoldPlayers')
    income_sold_players_commission: int = HTField('IncomeSoldPlayersCommission')
    income_sum: int = HTField('IncomeSum')
    costs_arena: int = HTField('CostsArena')
    costs_players: int = HTField('CostsPlayers')
    costs_financial: int = HTField('CostsFinancial')
    costs_bought_players: int = HTField('CostsBoughtPlayers')
    costs_arena_building: int = HTField('CostsArenaBuilding')
    costs_staff: int = HTField('CostsStaff')
    costs_youth: int = HTField('CostsYouth')
    costs_sum: int = HTField('CostsSum')
    expected_weeks_total: int = HTField('ExpectedWeeksTotal')
    last_income_spectators: int = HTField('LastIncomeSpectators')
    last_income_sponsors: int = HTField('LastIncomeSponsors')
    last_income_financial: int = HTField('LastIncomeFinancial')
    last_income_sold_players: int = HTField('LastIncomeSoldPlayers')
    last_income_sold_players_commission: int = HTField('LastIncomeSoldPlayersCommission')
    last_income_sum: int = HTField('LastIncomeSum')
    last_costs_arena: int = HTField('LastCostsArena')
    last_costs_players: int = HTField('LastCostsPlayers')
    last_costs_financial: int = HTField('LastCostsFinancial')
    last_costs_bought_players: int = HTField('LastCostsBoughtPlayers')
    last_costs_arena_building: int = HTField('LastCostsArenaBuilding')
    last_costs_staff: int = HTField('LastCostsStaff')
    last_costs_youth: int = HTField('LastCostsYouth')
    last_costs_sum: int = HTField('LastCostsSum')
    last_weeks_total: int = HTField('LastWeeksTotal')
