from pychpp.models.xml.match_details import MatchDetails


def test_get_future_match_details(mocked_chpp):
    md = mocked_chpp.xml_match_details(744337584)

    assert isinstance(md, MatchDetails)
    assert md.match.finished_date is None
