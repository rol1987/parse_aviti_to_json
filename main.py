import avito
import schedule
import way_to_file

def main(frequency):
    avito.get_data()
    # schedule.every().day.at("17:19").do(avito.get_data, number_pages)
    print('START')
    schedule.every(frequency).minutes.do(avito.get_data)

    while True:
        schedule.run_pending()
    
if __name__ == '__main__':
    def start():
        way_settings = way_to_file.way_settings()
        file_settings = open(way_settings, "r", encoding='utf-8')
        line = file_settings.readlines()
        frequency = int(line[1])
        file_settings.close
        main(frequency)
    start()

def restart():
    way_settings = way_to_file.way_settings()
    file_settings = open(way_settings, "r", encoding='utf-8')
    line = file_settings.readlines()
    frequency = int(line[1])
    file_settings.close
    main(frequency)