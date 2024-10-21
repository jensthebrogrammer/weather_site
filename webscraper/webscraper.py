from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Webscraper:       # classe die alle data gaat vinden en formatten
    def __init__(self, location):
        self.location = location        # de url van de site
        self.soup = None

    def get_daily_forecast(self):
        # get the part of the html that contains the data
        data_container = self.soup.find_all('div', class_='flex overflow-x-scroll')

        # create empty containers
        time_of_day = []
        temp_of_time = []
        rain_of_time = []

        for scroll_bar in data_container:   # scroll_bar is the scrolling bar on the site
            bar = scroll_bar.find_all('div', class_='items-center')     # one of the bars
            for data_block in bar:      # a single block in the scrolling bar
                # get the time
                time_ = data_block.find('span', class_='text-sm')
                for a_time in time_:
                    if a_time and len(a_time.text) > 4:     # to filter out the wrong data
                        time_of_day.append(a_time.text)
                    else:
                        time_of_day.append(None)        # None has to be added so that the other data stays in sync

                # get the temp
                temp = data_block.find('span', class_='text-secondary')
                if temp:        # if it contains data
                    temp_of_time.append(temp.text)
                else:
                    temp_of_time.append(None)

                # get the rain
                rain_div = data_block.find('div', class_='flex items-center gap-1 text-secondary h-8')
                if rain_div:        # if the container of the data contains something
                    rain_span = rain_div.find('span', class_='text-sm')
                    if rain_span:   # just checking if the data is valid
                        rain_of_time.append(rain_span.text)
                    else:
                        rain_of_time.append(None)
                else:
                    rain_of_time.append(None)

            # filtering the data
            i = 0
            while i < len(time_of_day):
                # if all the data in the index is invalid
                if not time_of_day[i] and not temp_of_time[i] and not rain_of_time[i]:
                    # remove the data
                    time_of_day.pop(i)
                    temp_of_time.pop(i)
                    rain_of_time.pop(i)
                i += 1

            # formatting the data
            data_to_return = {}
            for i in range(len(time_of_day)):
                data_to_return[time_of_day[i]] = dict(temp=temp_of_time[i], rain=rain_of_time[i])

            return data_to_return

    def use_driver(self, wanted_data):     # mijn google driver openen
        service = Service(ChromeDriverManager().install())  # de manager voor je google driver
        driver = webdriver.Chrome(service=service)  # opend de google driver voor de url op te zoeken
        driver.get(url=self.location)   # opend de opgegeven pagina

        html = driver.page_source   # de volledige html code van de pagina
        self.soup = bs(html, 'lxml')    # maakt het makkelijk om de html te lezen

        returned_data = []
        for func in wanted_data:
            returned_data.append(func())  # run every function that we need

        driver.quit()
        return returned_data # forwarding the data
