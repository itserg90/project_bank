def __main__():
    import utils

    json_obj = 'https://www.jsonkeeper.com/b/OZIQ'

    list_dicts = utils.get_json(json_obj)
    return utils.print_operation(list_dicts)


if __name__ in "__main__":
    print(*__main__(), sep='\n')
