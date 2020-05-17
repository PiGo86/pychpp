class HTRank:
    """
    Rank in Hattrick league
    """

    def __init__(self, user_ht_id, team_ht_id, team_name, position,
                 position_change, matches, goals_for, goals_against,
                 points, won, draws, lost):
        self.user_ht_id = user_ht_id
        self.team_ht_id = team_ht_id
        self.team_name = team_name
        self.position = position
        self.position_change = position_change
        self.matches = matches
        self.goals_for = goals_for
        self.goals_against = goals_against
        self.points = points
        self.won = won
        self.draws = draws
        self.lost = lost
