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
                    time = time and time.text.strip()

                    rain = (data_block.find('div', class_='flex items-center gap-1 text-secondary h-8')
                            or None)
                    rain = rain and rain.text.strip()

                    image = (data_block.find('img', class_='h-10 w-10 inline-block select-none align-top mt-4')
                             or None)
                    image = image and image.get('src')

                    temparature = data_block.find('span', class_='text-secondary') or None
                    temparature = temparature and temparature.text.strip()

                    if len(time) == 5:
                        data_map[time] = {'temp': temparature, 'rain': rain, 'img': image}

            except Exception as e:
                print(f'an error occured while mapping the data: {e}')
                return None

            return data_map

    def get_graph_data(self):
        try:
            rain_graph = self.soup.find('svg', class_='graph-svg')
            rain_path = rain_graph.find('path')
            graph_data = rain_path.get('d')

            return graph_data

        except Exception as e:
            print(f'the following error occurred when trying to get the graph data: {e}')
            return None

    def get_wind_direction(self):
        container = self.soup.find("div", class_='flex flex-col gap-2')
        data_block = container.find('div', class_="flex flex-row items-center")
        wind_direct_block = data_block.find('span', class_="text-md inline-block mr-2")
        wind_text = wind_direct_block.text.strip()
        wind_img = data_block.find('img', class_='w-6').get('src')

        return {"wind-text": wind_text, "wind-img": wind_img}

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
