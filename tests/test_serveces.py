import json

from src.services import simple_search


def test_simple_search(transactions_data):
    result = simple_search("еда", transactions_data)
    expected_result = json.dumps([transactions_data[0], transactions_data[3]], ensure_ascii=False)
    assert result == expected_result


def test_empty_search_query(transactions_data):
    result = simple_search("", transactions_data)
    expected_result = json.dumps(transactions_data, ensure_ascii=False)
    assert result == expected_result


def test_invalid_input():
    result = simple_search("еда", None)
    expected_result = json.dumps({"error": "'NoneType' object is not iterable"}, ensure_ascii=False)
    assert result == expected_result
