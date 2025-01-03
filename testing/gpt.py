def get_temps_gpt(soup):
    # Find the grid that contains the weather data (time, temperature, rain)
    temp_grid = soup.find_all('div', class_='flex overflow-x-scroll')

    time_of_day = []
    temp_of_time = []
    rain_of_time = []

    for column in temp_grid:
        # Find each weather block (each block contains time, temperature, rain info)
        weather_blocks = column.find_all('div', class_='items-center')

        for block in weather_blocks:
            # Extract the time
            time_span = block.find('span', class_='text-sm')
            if time_span and len(time_span.text) > 4:  # Valid time string
                time_of_day.append(time_span.text)
            else:
                time_of_day.append("Unknown time")

            # Extract the temperature
            temp_span = block.find('span', class_='text-secondary')
            if temp_span:
                temp_of_time.append(temp_span.text)
            else:
                temp_of_time.append("Unknown temperature")

            # Extract the rain data (if exists)
            rain_div = block.find('div', class_='flex items-center gap-1 text-secondary h-8')
            if rain_div:
                rain_span = rain_div.find('span', class_='text-sm')
                if rain_span:
                    rain_of_time.append(rain_span.text)
                else:
                    rain_of_time.append("no rain")
            else:
                rain_of_time.append("no rain")