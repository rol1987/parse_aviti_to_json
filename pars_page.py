import bs4
import lxml
import re
import pandas as pd
import datetime
import way_to_file
import json

def pars_page(f, frequency, sity, room, min_floor, max_floor):
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
        ad_dic = {'ID': '',
                  'Дата размещения объявления': '',
                  'Время добавления записи в файл': '',
                  'Ссылка': '',
                  'Название объявления': '',
                  'Количество комнат': '',
                  'Площадь': '',
                  'Этаж': '',
                  'Этажность дома': '',
                  'Цена': '',
                  'Цена за кв. метр': '',
                  'Место нахождения': '',
                  'Станция метро': '',
                  'Аналитика Авито (рыночная цена)': '',
                  'Количество завершенных объявлений': ''}

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

        # Парсим название объявления
        ad_name = item.find('h3').text
        ad_name_split = ad_name.split(", ")

        # Из названия объявления достаем тип недвижимости: квартира/аппартамент/что-то иное
        if ad_name_split[0] in ad_name_split:
            try:
                ad_type = re.search(r'\d{1,2}', ad_name_split[0]).group(0)
                if int(ad_type) != room: continue
            except:
                ad_type = ad_name_split[0]    
        else:
            ad_type = ''

        # Из названия объявления достаем площадь недвижимости
        if ad_name_split[1] in ad_name_split:
            ad_area = int(re.search(r'\d{1,4}', ad_name_split[1]).group(0))
        else:
            ad_area = ''

        # Из названия объявления достаем этаж недвижимости
        if ad_name_split[2] in ad_name_split:
            ad_floor = int(re.search(r'\d{1,2}', ad_name_split[2]).group(0))
            ad_floor_total = re.search(r'/\d{1,2}', ad_name_split[2]).group(0)
            ad_floor_total = int(re.sub("/", "", ad_floor_total))
            if ad_floor_total < min_floor or ad_floor_total > max_floor: continue
        else:
            ad_floor = ''
            ad_floor_total = ''

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

        # Парсим количество завершенных объявлений (если это указано)
        if "завершённых" in item.text:
            print('Есть зевершенные')
            ad_completed = item.find('span', class_='iva-item-text-Ge6dR').text
        else:
            ad_completed = ''

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
        ad_dic['Этажность дома'] = ad_floor_total
        ad_dic['Количество завершенных объявлений'] = ad_completed
        ad_dic['Время добавления записи в файл'] = str(datetime.datetime.now()) 

        # наполняем список объявлений словарями
        ad_list.append(ad_dic)

    current_date = datetime.date.today()
    
    # Записываем во временный json
    with open(way_to_file.way_json_temt(), 'w', encoding='utf-8') as json_file_temp:
        data = json.dumps(ad_list, ensure_ascii=False, indent=4)
        json_file_temp.write(data)
    
    # Записываем в Exel
    xl = pd.ExcelFile(way_to_file.way_data())
    df = pd.DataFrame.from_dict(ad_list)
    df1 = xl.parse('Sheet1')
    newData = pd.concat([df1, df])
    newData.to_excel((way_to_file.way_data()), index=False)
    xl.close()

    # Записываем в json
    excel_data_df = pd.read_excel(way_to_file.way_data(), sheet_name='Sheet1')
    thisisjson = excel_data_df.to_json(orient='records')
    thisisdict = json.loads(thisisjson)
    with open(f'{way_to_file.way_json()}_{sity}_{current_date}.json', 'w', encoding='utf-8') as json_file:
        data = json.dumps(thisisdict, ensure_ascii=False, indent=4)
        json_file.write(data)

    # Вычисляем дату, когда данные со страницы были распарсены
    print(f"Парсинг страницы закончен в {datetime.datetime.now()}")
    return f'{ad_new} новых объявлений'