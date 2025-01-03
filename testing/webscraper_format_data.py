# we moeten een manier vinden om de data op een gemakkelijke manier door te sturen
# de data moet kunnen vervomt worden naar json
# ik stel voor dat we een classe maken voor het weer van de dag
# en een overlappende classe voor de data van de week
# classes moeten functies bevatten zoals het vinden van de data, om de zoveel tijd nieuw data halen,
# een formatter naar json,...

# ik stel voor dat je voor de data op te halen een functie gebruikt die een lijst van functies inneemt
# op die manier hoef je maar een keer je driver open te doen, en alleen de data halen die je nodig hebt

class Webscraper:
    def __init__(self, location):
        self.location = "https://www.buienalarm.nl/belgie/" + location

    def get_daily_forecast(self):
        pass

    def get_rain_forecast(self):
        pass

    def get_week_data(self):
        # de bedoeling dat dit de data van heel de week neemt
        pass

    def to_json(self):
        pass


def open_driver(wanted_data): # moet een lijst van functies worden
    # zorg hier ook dat de functie de data doorstuurt
    pass

