# voorlopig gaan we nog geen database aanmaken. we gaan gewoon via de backend de data halen en doorgeven.
# op die manier hoeven we geen gebruik te maken van een database. als we later deze data willen bijhouden of analyseren.
# dan moeten we wel een database aanmaken.

from config import app
from flask import request, jsonify
from webscraper.webscraper import Webscraper
from models import UniqueIcons


@app.route("/get_day_weather", methods=['POST'])
def get_day_weather():
    url = request.json.get("url")

    scraper = Webscraper(url)
    actions = [scraper.get_daily_forecast, scraper.get_graph_data, scraper.get_wind_direction]

    try:
        data = scraper.use_driver(actions)

        # data_uniqueIcons = UniqueIcons.query.all()

    except Exception as e:
        print(f'the following error occurred while getting the requested data: {e}')
        return jsonify({'message': "a problem occurred"}), 400

    return jsonify({"message": "success", "data": data}), 200


if __name__ == "__main__":
    app.run(debug=True)
