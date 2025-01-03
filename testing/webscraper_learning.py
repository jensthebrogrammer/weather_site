from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def basic_read(file):
    with open(file, 'r') as html_file:
        content = html_file.read()
        return content


def basic_beautiful_soup(file):
    with open(file, 'r') as html_file:
        content = html_file.read()
        soup = bs(content, 'lxml')
        tags_to_find = soup.find_all('script')

        return tags_to_find


def print_text_in_tags(tags):
    for tag in tags:
        print(tag.text)


def excircise1():
    with open('04-website.html', 'r') as website:
        content = website.read()
        soup = bs(content, 'lxml')

        paragrafs = soup.find_all('p')
        for p in paragrafs:
            button = p.button
            text_in_button = button.text
            print(text_in_button)


def using_request(url):
    html = requests.get(url)
    soup = bs(html.text, 'lxml')
    rain_graph = soup.find_all('svg', class_='graph-svg')
    print(rain_graph)


#using_request('https://www.buienalarm.nl/belgie/arendonk/23100')


def using_webdriver(url):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    time.sleep(0)

    html = driver.page_source

    soup = bs(html, 'lxml')

    rain_graph = soup.find_all('svg', class_='graph-svg')

    # Loop through found SVGs and print the "d" attributes
    for svg in rain_graph:
        path_elements = svg.find_all('path')
        for path in path_elements:
            d_attr = path.get('d')
            print(d_attr)  # Print the 'd' attribute

    # Close the browser window
    driver.quit()


# Call the function
using_webdriver('https://www.buienalarm.nl/belgie/arendonk/23100')
