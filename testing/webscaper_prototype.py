from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_data_from(url):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    html = driver.page_source
    soup = bs(html, 'lxml')

    get_rain_graph_data(soup)
    get_temps(soup)

    driver.quit()


def get_rain_graph_data(soup):
    rain_graph = soup.find_all('svg', class_='graph-svg')
    for element in rain_graph:
        rain_path = element.find_all('path')
        for data in rain_path:
            graph_data = data.get('d')

            print(f'inside {rain_graph} the following path was found:\n {rain_path}')
            print(f'and this was the graph data: {graph_data}')


def get_temps(soup):
    temp_grid = soup.find_all('div', class_='flex overflow-x-scroll')
    time_of_day = []
    temp_of_time = []
    rain_of_time = []

    for column in temp_grid:
        data = column.find_all('div', class_='items-center')
        for data_block in data:
            time_span = data_block.find('span', class_='text-sm')
            for a_time in time_span:
                if a_time and len(a_time.text) > 4:
                    time_of_day.append(a_time.text)
                else:
                    time_of_day.append(None)

            temp = data_block.find('span', class_="text-secondary")
            if temp:
                temp_of_time.append(temp.text)
            else:
                temp_of_time.append(None)

            rain_div = data_block.find('div', class_='flex items-center gap-1 text-secondary h-8')
            if rain_div:
                rain_span = rain_div.find('span', class_='text-sm')
                if rain_span:
                    rain_of_time.append(rain_span.text)
                else:
                    rain_of_time.append(None)
            else:
                rain_of_time.append(None)

    i = 0
    while i < len(time_of_day):
        if not time_of_day[i] and not temp_of_time[i] and not rain_of_time[i]:
            time_of_day.pop(i)
            temp_of_time.pop(i)
            rain_of_time.pop(i)
        i += 1

    for i in range(len(time_of_day)):
        print(f"at {time_of_day[i]} the temp was {temp_of_time[i]} and the rain was {rain_of_time[i]}")
    return


get_data_from('https://www.buienalarm.nl/belgie/arendonk/23100')
