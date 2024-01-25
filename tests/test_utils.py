from src import utils
import datetime


def test_get_date_and_time():
    assert utils.get_date_and_time({}) == datetime.datetime(1970, 1, 1)
    assert utils.get_date_and_time({"date": "2021-10-10"}) == datetime.datetime(2021, 10, 10, 0, 0)


def test_sort_json():
    assert utils.sort_json([{}])


def test_get_state():
    assert utils.get_state({}) == KeyError
    assert utils.get_state({"state": "EXECUTED"}) == "EXECUTED"


def test_change_date_and_time():
    assert utils.change_date_and_time(datetime.datetime(1970, 1, 1)) == "01.01.1970"


def test_get_from():
    assert utils.get_from({}) == ""
    assert utils.get_from({"from": "EXECUTED"}) == "EXECUTED"


def test_get_to():
    assert utils.get_to({}) == ""
    assert utils.get_to({"to": "1111"}) == "1111"


def test_change_from_or_to():
    assert utils.change_from_or_to("Счет 00000000000000000000") == "Счет **0000"
    assert utils.change_from_or_to("Visa 0000000000000000") == "Visa 0000 00** **** 0000"


def test_get_description():
    assert utils.get_description({"description": "Operation"}) == "Operation"
    assert utils.get_description({}) == KeyError


def test_operation_amount():
    assert utils.operation_amount({"operationAmount": {"amount": 1_000, "currency": {"name": "RUB"}}}) == "1000 RUB"
    assert utils.operation_amount({})


def test_print_operation():
    assert utils.print_operation([{}]) == []
    assert utils.print_operation([{
        "id": 1,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589"
        }
    ]) == ["26.08.2019 Перевод организации\n"
           "Maestro 1596 83** **** 5199 -> Счет **9589\n"
           "31957.58 руб.\n"
           ]
    assert utils.print_operation([{
        "id": 441945886,
        "state": "CANCELED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589"
    }]) == []
