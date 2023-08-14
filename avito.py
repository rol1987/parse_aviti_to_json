from fake_headers import Headers
import way_to_file
import connect_and_save
import pars_page

def get_data():

    # Путь к файлам
    way_html = way_to_file.way_html()
    way_chromedriver = way_to_file.way_chromedriver()
    way_settings = way_to_file.way_settings()

    # Откроем файл с настройками и возьмем от туда URL
    file_settings = open(way_settings, "r", encoding='utf-8')
    line = file_settings.readlines()
    sity = line[0]
    file_settings.close

    # Скачиваем страницу
    url = f"https://www.avito.ru/{sity}/kvartiry/prodam/vtorichka-ASgBAQICAUSSA8YQAUDmBxSMUg?f=ASgBAQICAkSSA8YQwMENuv03AkDmBxSMUpC~DRSWrjU&s=104"
    
    print("URL получен")
    driver = connect_and_save.connect(url, way_chromedriver)

    # Записываем страницу в файл
    with open(way_html, 'w', encoding='utf-8') as file_write:
        file_write.write(driver.page_source)

    # Читаем файл
    with open(way_html, 'r', encoding='utf-8') as file_read:
        f = file_read.read()

    # Парсим и записываем в Excel
    pars_page.pars_page(f)