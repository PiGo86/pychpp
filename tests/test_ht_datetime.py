import datetime as dt
import pytz

from pychpp.ht_datetime import HTDatetime


def test_use_ht_datetime():

    ht_d = HTDatetime(datetime=dt.datetime(year=2020, month=9, day=7))
    assert (ht_d.season, ht_d.week, ht_d.weekday) == (75, 15, 1)
    assert ht_d.league == ""

    ht_d.league = "Brazil"
    assert ht_d.season == 63
    assert ht_d.league == "Brazil"

    ht_d = ht_d + dt.timedelta(days=900)
    assert (ht_d.season, ht_d.week, ht_d.weekday) == (71, 15, 5)
    cet = pytz.timezone("CET")
    date = cet.localize(dt.datetime(year=2023, month=2, day=24))
    assert ht_d.datetime == date
    assert ht_d.league == "Brazil"

    ht_d.timezone = "America/Belize"
    assert ht_d == HTDatetime.from_calendar(2023, 2, 23, 17,
                                            timezone="America/Belize")
    assert (ht_d.season, ht_d.week, ht_d.weekday) == (71, 15, 4)

    ht_d = HTDatetime.from_calendar(2020, 9, 21, 1, 30)
    assert (ht_d.season, ht_d.week, ht_d.weekday) == (76, 1, 1)
    ht_d.timezone = "America/Bahia"
    assert (ht_d.season, ht_d.week, ht_d.weekday) == (75, 16, 7)
