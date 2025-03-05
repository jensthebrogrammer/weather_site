from bs4 import BeautifulSoup as Bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from collections import defaultdict
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time

# i'm adding some settings that make this bot harder to detect
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent bot detection
options.add_argument("--headless")  # Run in the background (optional)
options.add_argument("--log-level=3")  # Reduce log spam
options.add_argument("--disable-gpu")  # Improves performance
options.add_argument("--no-sandbox")  # Bypass some security settings
options.add_argument("--disable-dev-shm-usage")  # Prevent crashes


class Webscraper:
    def __init__(self, url, file_name):
        # i made url private so i can reboot the driver anytime the user changes the url
        # i don't use it to validate the url because there is no concrete way to know that the url is valid
        self.__url = url

        # defining some privates
        self.__file_name = None
        self.__set_file_name(file_name)
        self.__driver_open = False  # om te voorkomen dat de driver meerdere keren geopend word

        # defining the driver
        self.__driver = None

        # root and target are for knowing in which part of the HTML u are
        # i'm not sure if i need to define a root here since i am always gonna fetch the HTML again
        # after the user wants data
        # however i'm keeping it in in case i ever add a functionality that doesn't need to fetch again
        self.__root = None

    @property
    def url(self):
        return self.__url

    # when the url is changed, the driver will reboot and use the correct url
    @url.setter
    def url(self, value):
        self.__url = value

        # reboot the driver with delay to make sure the driver fully shuts down first
        self.driver_off()
        time.sleep(0.5)
        self.driver_on()

    @property
    def file_name(self):
        return self.__file_name

    @file_name.setter
    def file_name(self, name):
        # ifinstance checks if it is the right type of value
        if isinstance(name, str) and len(name) > 0:
            self.__file_name = name
        else:
            print("filename is not valid")

    def __set_file_name(self, file_name):
        self.file_name = file_name

    # the user needs to turn of the driver if he wants to use the scraping functions
    def driver_on(self):
        # if the driver is already open the function won't do anything
        if not self.__driver_open:
            try:
                service = Service(ChromeDriverManager().install())  # de manager voor je google driver
                self.__driver = webdriver.Chrome(service=service)  # opend de google driver voor de url op te zoeken

                # setting the driver as open
                self.__driver_open = True

                self.__driver.get(url=self.url)   # opend de opgegeven pagina
                WebDriverWait(self.__driver, 10).until(
                    ec.presence_of_element_located((By.CLASS_NAME, "scroll-content"))
                )

                html = self.__driver.page_source   # de volledige html code van de pagina
                self.__root = Bs(html, 'lxml')    # maakt het makkelijk om de html te lezen
            except Exception as e:
                print(f'the following error occurred when booting the driver: {e}')
                quit()

    def driver_off(self):
        # it will only try to shut down if the driver is open
        if self.__driver_open:
            try:
                self.__driver.quit()
                self.__driver_open = False
            except Exception as e:
                print(f"an error occured while shuting down the driver: {e}")

    def get_daily_forecast(self):
        # if the root isn't updated yet
        if not self.__root:
            # if the root is empty, then that means that the driver hasn't been turned on yet
            # i'm not sure what the best thing to do is then, but for now i just turn it on myself
            self.driver_on()

        # make sure i'm in the right part of the html
        location = self.__root.find(id="block-10694")

        # get the part of the html that contains the data
        data_container = location.find('div', class_='flex overflow-x-scroll')
        data_map = {
                "timeTable": self.__scrape_scroll_bar(data_container),
                "windDirection": self.get_wind_direction()
            }

        # write to a file for seperate use
        self.__save(data_map)

        return data_map

    def get_wind_direction(self):
        # if the root isn't updated yet
        if not self.__root:
            self.driver_on()

        container = self.__root.find("div", class_='flex flex-col gap-2')
        data_block = container.find('div', class_="flex flex-row items-center")
        wind_direct_block = data_block.find('span', class_="text-md inline-block mr-2")
        wind_text = wind_direct_block.text.strip()
        wind_img = data_block.find('img', class_='w-6').get('src')

        self.__save({"wind-text": wind_text, "wind-img": wind_img})
        return {"wind-text": wind_text, "wind-img": wind_img}

    # this code gets a string of data from the site that can be used to make a graph
    def get_graph_data(self):
        try:
            rain_graph = self.__root.find('svg', class_='graph-svg')
            rain_path = rain_graph.find('path')
            graph_data = rain_path.get('d')     # getting the string

            # saving the data to a seperate file
            self.__save({"graph": graph_data})
            return graph_data

        except Exception as e:
            print(f'the following error occurred when trying to get the graph data: {e}')
            return None

    def get_weekly_weather(self):
        # this line finds the specific container i am looking for
        location = self.__root.find(id="block-10719")
        # this is the place where i can loop trough the content
        container = location.find('div', class_='flex flex-col mt-4')

        data_to_return = defaultdict(object)    # om de data in op te slagen

        # vind alle scrollbars van de week en zet het in een lijst
        days = container.find_all('div', class_='day mt-4')

        # looping trough 7 days
        for i in range(7):
            # het dagvak vinden
            passed_data = days[i].find('div', class_='scroll-x flex items-center')
            data_to_return[f"day{i+1}"] = self.__scrape_scroll_bar(passed_data)

        return data_to_return

    # private because the user doesn't need this function
    @staticmethod
    def __scrape_scroll_bar(container):
        # where all the sraped data gets mapped to
        data_map = {}

        # check if the passed container is not Null
        if not container:
            print("Error: Container not found!")
            return {}

        # the method for finding the data bars in the srollbar is slightly different
        # between doing it for the day and for the week
        if container.find('div', class_='py-2'):
            # bars are the individual elements in the scrollbar
            # find all makes a list of all the elements it finds with that description
            bars = container.find_all('div', class_='py-2')
        else:
            bars = container.find_all('div', class_='flex flex-col items-center py-4 px-3')

        # make 100% sure that we have data bars
        if not bars:
            print("Warning: No forecast blocks found!")
            return {}

        # loops trough the list of bars
        for bar in bars:
            try:
                time_tag = bar.find('span', class_='text-sm')
                # the special if statement is to make sure that it doesn't try to run
                # the strip() function on a Null
                time_stamp = time_tag.text.strip() if time_tag else None

                # Ensure valid time format before adding data
                # the html element of the time and the rain look the same so
                # we are making sure that we don't mix them up
                if time and len(time_stamp) == 5:
                    rain_container = bar.find('div', class_='flex items-center gap-1 text-secondary')
                    rain_tag = rain_container.find('span', class_='text-sm') if rain_container else None
                    rain = rain_tag.text.strip() if rain_tag else None

                    weather_icon = bar.find('img', class_='h-10 w-10 inline-block select-none align-top mt-4')
                    image = weather_icon['src'] if weather_icon else None  # Extract image URL

                    temp_tag = bar.find('span', class_='text-secondary')
                    temperature = temp_tag.text.strip() if temp_tag else None

                    # make a single piece of data
                    data_map[time_stamp] = {'temp': temperature, 'rain': rain, 'img': image}

            except Exception as e:
                print(f'An error occurred while mapping data: {e}')
                continue  # Continue scraping even if one block fails

        if not data_map:
            print("Warning: No valid weather data extracted.")

        return data_map  # Ensure return of dictionary

    def __save(self, content):
        try:
            with open(self.file_name, 'a') as document:
                for key, value in content.items():
                    document.write(f'{key}: {value}\n')

                document.write("\n\n\n")
        except Exception as e:
            print(f"something went wrong while saving to a file: {e}")
