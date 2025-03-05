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

<h3 style='color: green;'>
    Het volgende dataModel is om de gescrapte dagData mooi bij te houden en op te slagen. 
    dit doet het voor verschillende plekken en datums. deze database kan gebruikt worden om het
    weer te analyseren en grafieken te maken
</h3>
<h2 style='color: magenta;'>dayWeather:</h2>

> ## init:
> - id
> - location (geel, mol, arendonk, ...)
> - date (to keep track of when)
> - graph_string (de string die gebruikt word om ons grafie k te maken in de frontend)
> - time_tabel (de data van elke tijd. dit is dus ook een object)
> - wind_direction (the direction of the wind that day)
> 
> ## to_json():
> ```python
> return {
>   "graph_string": self.graph_string,
>   "time_table": self.time_table
> }

---

<h3 style='color: green;'>
    de volgende dataModel behoord tot de 'pre_fetch' dataBase. Deze houdt de huidige data van verschillende locaties bij zodat deze bij aanvraag direct klaar staan.
</h3>
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

<h3 style='color: green;'>
    Het volgende dataModel is het weer van de volgende 7 dagen bij te houden. Deze behoord tot de 'week_data' database.
    dit is gemakkelijk om de data van de volgende zeven dagen te bekijken.
</h3>
<h2 style='color: magenta;'>weekData:</h2>

>## init:
> - id
> - locatie
> - datum
> - dag1 = dayWeather()
> - ...
> - dag7 = dayWeather (alle zeven dagen apart bijhouden)
> 
> ## to_json():
> ```python
> return {
>   "dag1": self.dag1,
>   "...": self....,
>   "dag7": self.dag7
> }
