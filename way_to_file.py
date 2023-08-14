import os
from sys import platform

# формируем путь к сохраняемому файлу html
def way_html():
    cwd = os.path.dirname(__file__)
    file_name = 'example.html'
    full_path = os.path.join(cwd, file_name)
    return full_path

# формируем путь к драйверу Chrome
def way_chromedriver():
    cwd = os.path.dirname(__file__)
    if platform == 'linux' or platform == 'linux2':
        file_name = 'chromedriver_linux64'
    else:    
        file_name = 'chromedriver.exe'
    full_path = os.path.join(cwd, file_name)
    return full_path

# формируем путь к файлу с настройками
def way_settings():
    cwd = os.path.dirname(__file__)
    file_name = 'settings.txt'
    full_path = os.path.join(cwd, file_name)
    return full_path

# формируем путь к файлу data.xlsx
def way_data():
    cwd = os.path.dirname(__file__)
    file_name = 'data.xlsx'
    full_path = os.path.join(cwd, file_name)
    return full_path

# формируем путь к файлу json_temp.json
def way_json():
    cwd = os.path.dirname(__file__)
    file_name = 'json_temp.json'
    full_path = os.path.join(cwd, file_name)
    return full_path

