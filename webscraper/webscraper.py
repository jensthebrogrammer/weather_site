from bs4 import BeautifulSoup as Bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from collections import defaultdict


class Webscraper:       # classe die alle data gaat vinden en formatten
    def __init__(self, location):
        self.location = location        # de url van de site
        self.soup = None

    def get_daily_forecast(self):
        # get the part of the html that contains the data
        data_container = self.soup.find_all('div', class_='flex overflow-x-scroll')

        # create empty containers
        data_map = defaultdict(object)

        for scroll_bar in data_container:   # scroll_bar is the scrolling bar on the site
            try:
                bar = scroll_bar.find_all('div', class_='items-center')     # one of the bars
                for data_block in bar:      # a single block in the scrolling bar
                    time = data_block.find('span', class_='text-sm') or None
                    time = (time and data_block.
                            find('span', class_='text-sm').text.strip())

                    rain = (data_block.find('div', class_='flex items-center gap-1 text-secondary h-8')
                            or None)
                    rain = (rain and data_block.
                            find('div', class_='flex items-center gap-1 text-secondary h-8').text.strip())

                    temparature = data_block.find('span', class_='text-secondary') or None
                    temparature = (temparature and data_block.
                                   find('span', class_='text-secondary').text.strip())

                    data_map[time] = {'temp': temparature, 'rain': rain}
            except Exception as e:
                print(f'an error occured while mapping the data: {e}')

            return data_map

    def get_graph_data(self):
        try:
            rain_graph = self.soup.find_all('svg', class_='graph-svg')
            for element in rain_graph:
                rain_path = element.find_all('path')
                for data in rain_path:
                    graph_data = data.get('d')

                    return graph_data
        except Exception as e:
            print(f'the following error occurred when trying to get the graph data: {e}')
            return None

    def use_driver(self, wanted_data):     # mijn google driver openen
        try:
            service = Service(ChromeDriverManager().install())  # de manager voor je google driver
            driver = webdriver.Chrome(service=service)  # opend de google driver voor de url op te zoeken
            driver.get(url=self.location)   # opend de opgegeven pagina

            html = driver.page_source   # de volledige html code van de pagina
            self.soup = Bs(html, 'lxml')    # maakt het makkelijk om de html te lezen
        except Exception as e:
            print(f'the following error occurred when booting the driver: {e}')
            quit()

        try:
            returned_data = []
            for func in wanted_data:
                returned_data.append(func())  # run every function that we need

            driver.quit()
            return returned_data    # forwarding the data
        except Exception as e:
            print(f'the following error occurred when executing the scraping functions: {e}')
