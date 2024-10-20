def test_xml_bookmarks(mocked_chpp):

    xml_bookmarks = mocked_chpp.xml_bookmarks()

    assert isinstance(xml_bookmarks.bookmark_list, list)

    bm = xml_bookmarks.bookmark_list[1]
    assert bm.id == '164714411'
    assert bm.type_id == 1
    assert bm.text == 'FC DOUKI'
    assert bm.text_2 == 'DADAKI'
    assert bm.object_id == '590540'
    assert bm.object_id_2 is None
    assert bm.object_id_3 is None
    assert bm.comment == 'Coupe de Bourgogne'
