<h3 style='color: green;'>
    het volgende dataModel behoord tot de database 'unique_icons'. Deze database houdt alle unieke icoontjes bij de gelinkt zijn aan events
</h3>

<h2 style="color: magenta;">UniqueIcons:</h2>
>### init:
> - id  (om de data te kunnen fetchen)
> - event  (regen, zon, wolken)
> - icon   (het symbool dat bij de event hoort)
>
>### to_json():
> ```python
> return {
>   "event": self.event,
>   "icon": self.icon
> }
>

---

<h3 style='color: green;'>Het volgende dataModel is om de gescrapte dagData mooi bij te houden en op te slagen</h3>
<h2 style='color: magenta;'>dayWeather:</h2>

> ## init:
> - id
> - graph_string (de string die gebruikt word om ons grafie k te maken in de frontend)
> - time_tabel (de data van elke tijd. dit is dus ook een object)
> 
> ## to_json():
> ```python
> return {
>   "graph_string": self.graph_string,
>   "time_table": self.time_table
> }

---

<h3 style='color: green;'>de volgende dataModel behoord tot de 'pre_fetch' dataBase. Deze houdt de huidige data van verschillende locaties bij zodat deze bij aanvraag direct klaar staan</h3>
<h2 style='color: magenta;'>preFetch:</h2>

>## init:
> - id (om de data terug te kunnen vinden)
> - locatie (verbonden aan waar je de data van vraagt)
> - data = dayWeather() (om de verbonden data op te slagen)
> 
> ## to_json():
> ```python
> return {
>   "locatie": self.locatie,
>   "data": self.data.to_json()
> }
>

---

<h3 style='color: green;'>Het volgende dataModel is het weer van de volgende 7 dagen bij te houden. Deze behoord tot de 'week_data' database</h3>
<h2 style='color: magenta;'>weekData:</h2>

>## init:
> - id
> - nog niet compleet want ik kan deze nog niet fetchen
