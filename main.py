import avito

def restart(frequency, sity, room, min_floor, max_floor):
    avito.get_data(frequency, sity, room, min_floor, max_floor)

def start():
    sity = input('Введите город (например moskva): ')
    room = int(input('Количество комнат в квартире: '))
    min_floor = int(input('Min rоличество этажей в доме :'))
    max_floor = int(input('Max rоличество этажей в доме :'))
    frequency = ""
    # frequency = int(input('Задайте частоту парсинга в минутах: '))
    res = avito.get_data(frequency, sity, room, min_floor, max_floor)
    return res