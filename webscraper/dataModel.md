## **Weather Forecast Data Model**

### **1. Next 24 Hours Forecast (Hourly Data)**

Each entry represents weather data for a specific hour within the next 24 hours.


| Time (HH:MM) | Temperature (°C/°F) | [Condition](#) (Link) | [Wind Direction](#) (Link) | Rain (%) |
| ------------ | --------------------- | --------------------- | -------------------------- | -------- |
| 00:00        | XX°C/XX°F           | [Clear](#)            | [North](#)                 | XX%      |
| 01:00        | XX°C/XX°F           | [Cloudy](#)           | [East](#)                  | XX%      |
| ...          | ...                   | ...                   | ...                        | ...      |
| 23:00        | XX°C/XX°F           | [Rainy](#)            | [West](#)                  | XX%      |

---

### **2. Next 7 Days Forecast (Daily Data)**

Each entry represents weather data for a specific day.


| Date (YYYY-MM-DD) | Temperature (°C/°F) | [Condition](#) (Link) | [Wind Direction](#) (Link) | Rain (%) |
| ----------------- | --------------------- | --------------------- | -------------------------- | -------- |
| YYYY-MM-DD        | XX°C/XX°F           | [Sunny](#)            | [North-East](#)            | XX%      |
| YYYY-MM-DD        | XX°C/XX°F           | [Cloudy](#)           | [South](#)                 | XX%      |
| ...               | ...                   | ...                   | ...                        | ...      |
| YYYY-MM-DD        | XX°C/XX°F           | [Stormy](#)           | [West](#)                  | XX%      |
