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


# initialize the websraper
scraper = Webscraper('https://www.buienalarm.nl/belgie/arendonk/23100', "../testing/test_file_name.txt")

# making location so i can fabricate urls easier
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
                scraper.url = "https://www.buienalarm.nl/belgie" + value[0]

                # fetching the data
                day_data = scraper.get_daily_forecast()
                graph_data = scraper.get_graph_data()
                week_data = scraper.get_weekly_weather()

                # making the prefetch
                if PreFetch.query.filter_by(_id=value[1]).first():  # if there is already some data there
                    try:
                        # replace the old data
                        data_to_alter = PreFetch.query.filter_by(_id=value[1]).first()    # finding the right id
                        data_to_alter.data = DayWeather(
                                                location=key,
                                                date=datetime.today().date(),
                                                graph_string=graph_data,
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
                                graph_string=graph_data,
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


# this code still needs to reviewed and changed
@app.route("/get_day_weather", methods=['POST'])
def get_day_weather():
    url = request.json.get("url")

    # changing the url of the scraper
    scraper.url = url

    try:
        scraper.driver_on()
        data = {
            "today": scraper.get_daily_forecast(),
            "week": scraper.get_weekly_weather()
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


if __name__ == "__main__":
    # the app needs this context line in order to run db.create_all
    with app.app_context():
        db.create_all()
        app.run(debug=True)
