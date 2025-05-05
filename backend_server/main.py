# i'm going to declare 3 different scrapers. one for the short cycle, one for the long one
# and one for the server itself. this way these pieces of code can work independedly

from config import app, db
from flask import request, jsonify
from webscraper.webscraper import Webscraper
from models import DayWeather, WeekData, PreFetch
import threading
import time
from datetime import datetime
import random
import schedule


# initialize the websrapers
scraper_short_cycle = Webscraper('https://www.buienalarm.nl/belgie/arendonk/23100', "../testing/test_file_name.txt")
scraper_server = Webscraper('https://www.buienalarm.nl/belgie/arendonk/23100', "../testing/test_file_name.txt")

# making the locations, so I can fabricate urls easier
# the numbers are for defining the id's of the data
locations = {
    "arendonk": ['/arendonk/23100', 23100],
    "mol": ["/mol/13899", 13899],
    "dessel": ['/dessel/23120', 23120],
    "geel": ["/geel/23138", 23138],
    "retie": ["/retie/16447", 16447]
}


# this piece of code is responsible for fetchening the data every few minutes
# so that there is always fresh data available for these locations
def short_cycle():
    # keep looping
    while True:
        with app.app_context():  # Zorg ervoor dat SQLAlchemy correct werkt binnen een thread
            # looping trough every location
            for key, value in locations.items():
                # when the url of the scraper is changed the scraper automaticly reboots the driver into the right url
                scraper_short_cycle.url = "https://www.buienalarm.nl/belgie" + value[0]

                # fetching the data
                day_data = scraper_short_cycle.get_daily_forecast()
                week_data = scraper_short_cycle.get_weekly_weather()

                # making the prefetch
                if PreFetch.query.filter_by(_id=value[1]).first():  # if there is already some data there
                    try:
                        # replace the old data
                        data_to_alter = PreFetch.query.filter_by(_id=value[1]).first()    # finding the right id
                        data_to_alter.data = DayWeather(
                                                location=key,
                                                date=datetime.today().date(),
                                                graph_string=day_data["graphString"],
                                                time_table=day_data["timeTable"],
                                                wind_direction=day_data['windDirection']
                                            ).to_json()

                        # updating the database
                        db.session.commit()
                    except Exception as e:
                        print(f'something went wrong while altering the prefetch: {e}')
                else:
                    # if there is no data with this id yet
                    try:
                        # making a single piece of data
                        new_pre_fetch = PreFetch(
                            data=DayWeather(
                                location=key,
                                date=datetime.today().date(),
                                graph_string=day_data["graphString"],
                                time_table=day_data["timeTable"],
                                wind_direction=day_data['windDirection']
                            ).to_json()
                        )

                        # setting the id manually
                        new_pre_fetch._id = value[1]

                        # adding the new data to the database
                        db.session.add(new_pre_fetch)
                        db.session.commit()
                    except Exception as e:
                        print(f'something went wrong while trying to add a new prefetch: {e}')

                # updating the weekdata database
                if WeekData.query.filter_by(_id=value[1]).first():
                    try:
                        # replace the old data
                        data_to_alter = WeekData.query.filter_by(_id=value[1]).first()    # finding the right id

                        # setting the location and date
                        data_to_alter.location = key
                        data_to_alter.date = datetime.today().date()

                        data_to_alter.day1 = week_data["day1"]
                        data_to_alter.day2 = week_data["day2"]
                        data_to_alter.day3 = week_data["day3"]
                        data_to_alter.day4 = week_data["day4"]
                        data_to_alter.day5 = week_data["day5"]
                        data_to_alter.day6 = week_data["day6"]
                        data_to_alter.day7 = week_data["day7"]

                        # updating the database
                        db.session.commit()
                    except Exception as e:
                        print(f'something went wrong while trying to alter weekdata: {e}')
                else:
                    try:
                        # making a new piece of weekdata
                        new_week_data = WeekData(
                            location=key,
                            date=datetime.today().date(),
                            day1=week_data["day1"],
                            day2=week_data["day2"],
                            day3=week_data["day3"],
                            day4=week_data["day4"],
                            day5=week_data["day5"],
                            day6=week_data["day6"],
                            day7=week_data["day7"]
                        )

                        new_week_data._id = value[1]

                        # adding the new piece of data to the database
                        db.session.add(new_week_data)
                        db.session.commit()
                    except Exception as e:
                        print(f'something went wrong while trying to add new weekdata: {e}')

                # making sure bot doesn't go to fast
                time.sleep(random.randint(4, 7)*60 + random.randint(4, 59))

            # randomizing the delay to make it look human
            random_delay = random.randint(6, 8)*60 + random.randint(1, 59)
            time.sleep(random_delay)


# start the thread. this makes a piece of code run seperately
thread1 = threading.Thread(target=short_cycle, daemon=True)
# starting the thread
thread1.start()


# making the daily cycle
def daily_fetch():
    # looping trough every location
    for key, value in locations:
        # getting the right data in json format
        weather_data = PreFetch.query.filter_by(_id=value[1]).first().to_json()

        # defining the data pieces
        graph_string = weather_data.data.graph_string
        time_table = weather_data.data.time_table
        wind_direction = weather_data.data.wind_direction

        # putting the data in the right format
        # the id gets assigned by sql because its teh primary key
        data_to_add = DayWeather(
            location=key,
            date=datetime.today().date(),
            graph_string=graph_string,
            time_table=time_table,
            wind_direction=wind_direction
        )

        # adding the data
        db.session.add(data_to_add)

    # I only commit when all the data is processed
    db.session.commit()


# schedule makes it run a function every day
# i've set it to midnight because get_daily_forecast is for the next 24 ours
schedule.every().day.at("00:05").do(daily_fetch)


# this cycle only check if it the next day yet
def long_cycle():
    while True:
        schedule.run_pending()
        time.sleep(120)


# start the thread. this makes a piece of code run seperately
thread2 = threading.Thread(target=long_cycle, daemon=True)
# starting the thread
thread2.start()

# fix the verification of foreign adresses
def verify_url_id(url):
    try:
        list_url = list(url)
        string_id = ""

        for i in range(5):
            string_id += list_url[-5 + i]

        for key, value in locations.items():
            if int(string_id) == value[1]:
                return value[1]

        return False
    except Exception as e:
        print(f"foreign adrres found: {e}")
        return False


# this route is used when someone wants to access weather data
# if the wanted data is in the pre_fetch it will get it there
# if not, it wil get it via the scraper
@app.route("/get_day_weather", methods=['POST'])
def get_day_weather():
    # get the url the user is trying to access
    url = request.json.get("url")

    # checking if the url is in the pre_fetch
    verification = verify_url_id(url)

    # if it is, this code will run
    if verification:
        try:
            # use the pre_fetch to get the data
            today = PreFetch.query.filter_by(_id=verification).first().to_json()
            week = WeekData.query.filter_by(_id=verification).first().to_json()

            # putting it in a font
            data = {
                'today': today["data"],
                "week": week
            }

            return jsonify({"data": data, "message": "success"})
        except Exception as e:
            print(f"something went wrong while trying to access the pre_fetch: {e}")

    # changing the url of the scraper
    scraper_server.url = url

    try:
        # getting the data manually
        scraper_short_cycle.driver_on()
        data = {
            "today": scraper_server.get_daily_forecast(),
            "week": scraper_server.get_weekly_weather()
        }

    except Exception as e:
        print(f'the following error occurred while getting the requested data: {e}')
        return jsonify({'message': "a problem occurred"}), 400

    return jsonify({"message": "success", "data": data}), 200


# a route to get the pre_fetch data
@app.route("/pre_fetch", methods=["GET"])
def pre_fetch():
    # getting all the available data
    data = PreFetch.query.all()

    # this line turns all the data in the right json format
    passed_data = list(map(lambda x: x.to_json(), data))

    return jsonify({"data": passed_data}), 200


# take a look at pre_fetch()
@app.route("/week_data_vieuw", methods=["GET"])
def week_data_vieuw():
    data = WeekData.query.all()
    passed_data = list(map(lambda x: x.to_json(), data))

    return jsonify({"data": passed_data}), 200


@app.route("/get_dayweather", methods=['GET'])
def get_dayweather():
    data = DayWeather.query.all()
    passed_data = list(map(lambda x: x.to_json(), data))

    return jsonify({"data": passed_data})


if __name__ == "__main__":
    # the app needs this context line in order to run db.create_all
    with app.app_context():
        db.create_all()
        app.run(debug=True)
