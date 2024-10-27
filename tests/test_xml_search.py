def test_search(mocked_chpp):

    search = mocked_chpp.xml_search(search_type=0,
                                    search_string='Bob',
                                    search_string_2='Sunesson',
                                    search_league_id=-1,
                                    )

    assert search.page_index == 0
    assert search.pages == 1

    assert search.search_params.type == 0
    assert search.search_params.string == "Bob"
    assert search.search_params.string_2 == "Sunesson"
    assert search.search_params.id == 0
    assert search.search_params.league_id == -1

    assert len(search.search_results) == 5
    assert search.search_results[0].id == 336960433
    assert search.search_results[0].name == "Bob Sunesson"
