from webscraper.webscraper import Webscraper


def testing_webscraper():
    my_scraper = Webscraper('https://www.buienalarm.nl/belgie/arendonk/23100')

    wanted_data = [my_scraper.get_daily_forecast, my_scraper.get_graph_data]
    data = my_scraper.use_driver(wanted_data)
    for key, value in data[0].items():
        print(f'{key}: {value}')

    print(f'this is the graph data {data[1]}')


testing_webscraper()
