import time


def testing_scraper(url):
    from webscraper.webscraper import Webscraper

    my_scraper = Webscraper(url, "test_file_name.txt")

    my_scraper.driver_on()
    data = my_scraper.get_daily_forecast()
    graph = my_scraper.get_graph_data()
    weekly_forecast = my_scraper.get_weekly_weather()

    for key, value in data["timeTable"].items():
        print(f'{key}: {value}')

    print(data["windDirection"])

    print(graph)

    for i in range(7):
        print(f"day{i+1}")
        for value in weekly_forecast[f"day{i+1}"].items():
            print(value)

        print("\n\n\n\n")




    my_scraper.url = "https://www.buienalarm.nl/belgie/mol/13899"

    data = my_scraper.get_daily_forecast()
    graph = my_scraper.get_graph_data()
    weekly_forecast = my_scraper.get_weekly_weather()

    for key, value in data["timeTable"].items():
        print(f'{key}: {value}')

    print(data["windDirection"])

    print(graph)

    for i in range(7):
        print(f"day{i + 1}")
        for value in weekly_forecast[f"day{i + 1}"].items():
            print(value)

        print("\n\n\n\n")

    my_scraper.driver_off()


start = time.time()
testing_scraper('https://www.buienalarm.nl/belgie/arendonk/23100')
stop = time.time()

print(stop-start)
