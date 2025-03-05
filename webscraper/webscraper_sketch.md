````mermaid
classDiagram
    class Webscraper {
        - __url: str
        - __root: BeautifulSoup
        - __driver_open: bool
        - __file_name: str
        - __driver: WebDriver

        + url: str
        + file_name: str
        + set_file_name(name: str): void
        + get_daily_forecast(): dict
        + get_weekly_forecast(): dict
        + get_wind_direction(): dict
        + get_graph_data(): str
        + scrape_scrollbar(container: Tag): dict
        + use_driver(): void
        + driver_on(): void
        + driver_off(): void
        + __save(content: dict): void
    }
````

