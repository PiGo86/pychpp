import csv

from pychpp import CHPP

chpp = CHPP('ncvwg4pK2odKBt1hs6rinX',
            '9ALITe3uM7MPfvRTUobhiWtCig6iJ5SEyggOoD9SCMc',
            'of6CRWygunbWGoj5',
            'ybFbyLZ1jVyLGp2j',
            )

div_id_dict = {5: (21577, 21832),
               6: (35989, 37012),
               }

div_level = 6
rank = 1

div_id = div_id_dict[div_level]

data = []
for i in range(div_id[0], div_id[1] + 1):
    league = chpp.league(ht_id=i)

    for r in league.ranks:
        if r.position == rank:
            team = chpp.team(ht_id=r.team_ht_id)
            data.append({"league": league.name,
                         "team_id": r.team_ht_id,
                         "team_name": team.name,
                         "points": r.points,
                         "gf": r.goals_for,
                         "ga": r.goals_against,
                         "gavg": r.goals_for - r.goals_against
                         })

with open(f"div{div_level}_r{rank}.csv", 'w', newline='') as csvfile:
    fieldnames = data[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in data:
        writer.writerow(i)
