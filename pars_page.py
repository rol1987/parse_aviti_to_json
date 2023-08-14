import bs4
import lxml
from pprint import pprint
import re
import pandas as pd
import datetime
import telebot
import way_to_file
import emoji
import os
import json

def pars_page(f):
    print("начинаем парсить")
    soup = bs4.BeautifulSoup(f, 'lxml')

    # генерируем список всех объявлений на странице
    ad_card = soup.find_all('div', class_='iva-item-content-rejJg')

    # Из файла data.xlsx возьмем все ID и запишем их в список, с которым в дальнейшем будем сравнивать новые объявления и исключать повторения
    df = pd.read_excel(way_to_file.way_data(), sheet_name = 0)
    
    # Проверяем, есть ли объявления в файле или файл пустой?
    if 'ID' in df.columns:
        mylist = list(df['ID'])
    else:
        mylist = []
        print('В файле нет ни одного объявления')
    
    # Достаем информацию по каждому объявлению при помощи цикла for
    ad_list = []
    ad_link_list = []
    ad_analytics_price_list = []
    ad_price_list = []
    ad_new = 0
    for item in ad_card:
        # Создаем словарь
        ad_dic = {'ID': '', 'Дата размещения объявления': '', 'Время добавления записи в файл': '', 'Ссылка': '', 'Название объявления': '', 'Количество комнат': '', 'Площадь': '', 'Этаж': '', 'Цена': '', 'Цена за кв. метр': '', 'Место нахождения': '', 'Станция метро': '', 'Аналитика Авито (рыночная цена)': ''}

        # Парсим ссылку на объявление
        ad_link = f"https://www.avito.ru{item.find('a')['href']}"

        # Парсим ID объявления      
        ad_id = re.search(r'\._\d{4,}', ad_link).group(0)
        ad_id = int(re.sub("._", "", ad_id))

        # Проверяем, есть ли в excel-файле объявления с таким ID. Если есть, то пропускаем цикл
        if ad_id in mylist:
            continue
        else:
            ad_new += 1 # Считаем количество новых объявлений
            ad_link_list.append(ad_link) # Наполняем список ссылками объявлений для отправки в телеграмм
        print(f'{ad_new} новых объявлений!!!')

        # Парсим название объявления
        ad_name = item.find('h3').text
        ad_name_split = ad_name.split(", ")

        # Из названия объявления достаем тип недвижимости: квартира/аппартамент/что-то иное
        if ad_name_split[0] in ad_name_split:
            ad_type = ad_name_split[0]
        else:
            ad_type = ''

        # Из названия объявления достаем площадь недвижимости
        if ad_name_split[1] in ad_name_split:
            ad_area = ad_name_split[1]
        else:
            ad_area = ''

        # Из названия объявления достаем этаж недвижимости
        if ad_name_split[2] in ad_name_split:
            ad_floor = ad_name_split[2]
        else:
            ad_floor = ''

        # Парсим цену объявления
        ad_price = item.find('p', {"data-marker": "item-price"}).text
        ad_price = int(re.sub(r'\D', '', ad_price))
        ad_price_list.append(ad_price) # наполняем список ценами для отправки в телеграмм

        # Парсим цену за квадратный метр
        ad_price_per_metre = item.find('p', {"data-marker": False}, re.compile('.*м².*')).text
        ad_price_per_metre = int(re.sub(r'\D', '', ad_price_per_metre))

        # Парсим местоположение
        ad_geo = item.find('div', class_='geo-root-zPwRk').find('p').find('span').text
        
        # Парсим метро
        ad_metro = item.find_all('p')
        ad_metro = ad_metro[3].find('span', class_=None)
        if ad_metro == None:
            ad_metro = 'Метро не указано'
        else:
            ad_metro = ad_metro.text

        # Проверяем есть ли признак "рыночной цены" у объявления
        if "ыночная цена" in item.text:
            analytics_price = 'Рыночная цена'
        else:
            analytics_price = ''
        ad_analytics_price_list.append(analytics_price) # наполняем список для отправки в телеграмм

        # Парсим дату размещения объявления
        ad_data_marker = item.find('p', {"data-marker": "item-date"}).text

        # Записываем все данные по объявлению в словарь
        ad_dic['ID'] = ad_id
        ad_dic['Ссылка'] = ad_link
        ad_dic['Название объявления'] = ad_name
        ad_dic['Цена'] = ad_price
        ad_dic['Цена за кв. метр'] = ad_price_per_metre
        ad_dic['Место нахождения'] = ad_geo
        ad_dic['Станция метро'] = ad_metro
        ad_dic['Аналитика Авито (рыночная цена)'] = analytics_price
        ad_dic['Дата размещения объявления'] = ad_data_marker
        ad_dic['Количество комнат'] = ad_type
        ad_dic['Площадь'] = ad_area
        ad_dic['Этаж'] = ad_floor
        # ad_dic['Время добавления записи в файл'] = datetime.datetime.now() 

        # наполняем список объявлений словарями
        ad_list.append(ad_dic)

    
        # Записываем в json
    with open(way_to_file.way_json(), 'w', encoding='utf-8') as file:
        data = json.dumps(ad_list, ensure_ascii=False, indent=4)
        file.write(data)
    

    
    # Записываем в Exel
    # xl = pd.ExcelFile(way_to_file.way_data())
    # df = pd.DataFrame.from_dict(ad_list)
    # df1 = xl.parse('Sheet1')
    # newData = pd.concat([df1, df])
    # newData.to_excel((way_to_file.way_data()), index=False)

    # Вычисляем дату, когда данные со страницы были распарсены
    now = datetime.datetime.now()
    print(f"Страница распарсена в {now}")

    # Отправляем данные в телеграмм
    # token = f'6273197682:AAFtHg1veb8o8iWbIEXdgNEuXky8WQs1WHE'  
    # if ad_new > 0:
    #     bot = telebot.TeleBot(token)
    #     id_users = ['5139171378', '772382203']
    #     for id_user in id_users:
    #         try:
    #             bot.send_message(chat_id=id_user, text=[f'{ad_new} новых объявлений'])
    #             kol = 0
    #             for item in ad_link_list:
    #                 if ad_analytics_price_list[kol] == 'Рыночная цена':
    #                     bot.send_message(chat_id=id_user, text=f"{emoji.emojize(':thumbs_up:')} {ad_analytics_price_list[kol]}: {ad_price_list[kol]:,}\n{item}")
    #                 else:
    #                     bot.send_message(chat_id=id_user, text=f"Цена: {ad_price_list[kol]:,}\n{item}")
    #                 kol += 1
    #         except:
    #             print(f'Пользователь ID = {id_user} не нажал START в телеграм боте')
    #             continue  