import requests
import datetime


def get_json(name: str):
    """Получаем JSON-файл из облачного хранилища"""
    return requests.get(name).json()


def get_date_and_time(current_dict: dict):
    """Функция для ключа сортировки операций по дате, возвращаем тип datetime
    Получаем дату и приводим к типу datetime"""
    if "date" not in current_dict:
        return datetime.datetime(1970, 1, 1)
    return datetime.datetime.fromisoformat(current_dict["date"])


def sort_json(list_operations: list):
    """Сортировка операций по дате"""
    return sorted(list_operations, key=lambda x: get_date_and_time(x), reverse=True)


def change_date_and_time(current_date):
    """Приводим дату к удобному чтению для пользователя"""
    return datetime.datetime.strftime(current_date, "%d.%m.%Y")


def get_state(current_dict: dict):
    """Получаем статус выполнения операции(успешно, неуспешно)"""
    if "state" not in current_dict:
        return KeyError
    return current_dict["state"]


def get_from(current_dict: dict):
    """Получаем счет или номер карты откуда выполнен перевод"""
    if "from" not in current_dict:
        return ""
    return current_dict["from"]


def get_to(current_dict: dict):
    """Получаем счет или номер карты куда выполнен перевод или счет открытия"""
    if "to" not in current_dict:
        return ""
    return current_dict["to"]


def change_from_or_to(account_number: str):
    """Скрываем номер счета или карты"""
    if account_number:
        account, number = account_number.rsplit(maxsplit=1)
        if len(number) == 16:
            return f"{account} {number[:4]} {number[4:6]}** **** {number[-4:]}"
        return f"{account} **{number[-4:]}"


def get_description(current_dict: dict):
    """Получаем описание типа операции"""
    if "description" not in current_dict:
        return KeyError
    return current_dict["description"]


def operation_amount(current_dict: dict):
    """Получаем сумму и валюту и делаем удобным для чтения пользователем"""
    if "operationAmount" not in current_dict:
        return KeyError
    nested_dictionary = current_dict["operationAmount"]
    return f'{nested_dictionary["amount"]} {nested_dictionary["currency"]["name"]}'


def print_operation(list_dicts):
    count = 0
    list_operations = []

    for current_dict in sort_json(list_dicts):
        if count == 5:
            return list_operations

        status = get_state(current_dict)

        if status == "EXECUTED":
            date_operation = get_date_and_time(current_dict)
            current_date = change_date_and_time(date_operation)
            description = get_description(current_dict)
            from_operation = get_from(current_dict)
            to_operation = get_to(current_dict)
            currency_and_amount = operation_amount(current_dict)
            count += 1
            if from_operation:
                operation = f"{change_from_or_to(from_operation)} -> {change_from_or_to(to_operation)}"
            else:
                operation = f"{change_from_or_to(to_operation)}"
            list_operations.append(f"{current_date} {description}\n"
                                   f"{operation}\n"
                                   f"{currency_and_amount}\n")
    return list_operations
