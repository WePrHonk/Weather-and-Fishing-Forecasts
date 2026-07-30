import requests
from datetime import datetime

def search_city(city_name):
    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": city_name,
            "count": 5,
            "language": "en",
            "format": "json"
        }
    )

    data = response.json()

    if "results" not in data:
        return None

    return data["results"]
    
    
def calculate_time_score(hour):
    if 5 <= hour <= 9 or 18 <= hour <= 22:
        return 2.2
    elif hour == 23 or 0 <= hour < 5:
        return 1.5
    else:
        return 0.5


def calculate_temp_score(temp):
    if 20 <= temp <= 27:
        return 1.8
    elif 17 <= temp < 20 or 27 < temp <= 30:
        return 1
    else:
        return 0.5


def calculate_wind_speed_score(wind_speed):
    if 2 <= wind_speed <= 6:
        return 1.5
    elif wind_speed == 1 or wind_speed == 7:
        return 0.9
    else:
        return 0.5


def calculate_wind_direction_score(wind_direction):
    if 150 <= wind_direction <= 300:
        return 0.5
    else:
        return 0.3


def calculate_pressure_score(pressures):
    if len(pressures) < 2:
        return 0

    changes = []

    for i in range(1, len(pressures)):
        delta = pressures[i] - pressures[i - 1]
        changes.append(delta)

    avg_change = sum(changes) / len(changes)

    if avg_change < -2.0:
        return 3.5
    elif -2.0 <= avg_change <= -0.3:
        return 4.0
    elif -0.3 < avg_change < 0.3:
        return 3.0
    elif 0.3 <= avg_change <= 1.5:
        return 2.0
    else:
        return 1.0


def calculate_cloud_score(cloud):
    if 50 <= cloud <= 85:
        return 0.5
    elif 30 <= cloud < 50 or 85 < cloud <= 100:
        return 0.3
    else:
        return 0.1


while True:
    print("\n---- ENTER CITY NAME ----")

    name = input("Enter city name (or 0 to exit): ").strip()

    if name == "0":
        print("Exiting...")
        break

    cities = search_city(name)

    if cities is None:
        print("City not found!")
        continue
    
    if len(cities) == 1:
        selected = cities[0]
        print(f"Found: {selected['name']}, {selected.get('country', '')}")

    else:
        print("\nFound cities:")

    for i, city in enumerate(cities, start=1):
        country = city.get("country", "Unknown")
        admin1 = city.get("admin1", "")
        print(f"{i}. {city['name']}, {admin1}, {country}")

    while True:
        try:
            choice = int(input("Choose a city: "))

            if 1 <= choice <= len(cities):
                break
            else:
                print(f"Please enter a number from 1 to {len(cities)}.")

        except ValueError:
            print("Please enter numbers only!")

    selected = cities[choice - 1]

    lat = selected["latitude"]
    lon = selected["longitude"]
    name = selected["name"]


    while True:
        try:
            hour = int(input("Enter the hour (0-23): "))

            if 0 <= hour <= 23:
                print("")
                print("Fetching data...")
                break
            else:
                print("Enter a number from 0 to 23")

        except ValueError:
            print("Enter only a number!")

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,wind_speed_10m,precipitation,wind_direction_10m,pressure_msl,cloud_cover",
            "past_days": 1,
            "timezone": "auto",
        }
    )

    data = response.json()

    time_key = f"{datetime.now().strftime('%Y-%m-%d')}T{hour:02d}:00"

    times = data["hourly"]["time"]

    if time_key not in times:
        print("No data for this hour")
        continue

    index = times.index(time_key)
    start_index = max(0, index - 4)
    pressures_list = data["hourly"]["pressure_msl"][start_index : index + 1]
    temp = data["hourly"]["temperature_2m"][index]
    wind_speed = data["hourly"]["wind_speed_10m"][index]
    wind_direction = data["hourly"]["wind_direction_10m"][index]
    rain = data["hourly"]["precipitation"][index]
    pressures = data["hourly"]["pressure_msl"][index]
    cloud = data["hourly"]["cloud_cover"][index]

    time_score = calculate_time_score(hour)
    temp_score = calculate_temp_score(temp)
    wind_speed_score = calculate_wind_speed_score(wind_speed)
    wind_direction_score = calculate_wind_direction_score(wind_direction)
    pressure_score = calculate_pressure_score(pressures_list)
    cloud_score = calculate_cloud_score(cloud)

    score = round(time_score + temp_score + wind_speed_score + wind_direction_score + pressure_score + cloud_score, 1)

    print(f"\n🌍 City: {name}")
    print(f"📍 Coordinates: {lat}, {lon}")
    print(f"⏰ Hour: {hour}:00")
    print("------------------------------")
    print(f"🌡 Temperature: {temp}°C")
    print(f"💨 Wind Max Speed: {wind_speed} m/s  ({round(wind_speed*3.6, 1)} km/h)")
    print(f"🧭 Wind Direction: {wind_direction}°")
    print(f"🌧 Precipitation: {rain} mm")
    print(f"🌐 Pressure: {round(pressures * 0.75006, 1)} mmHg  ({pressures} hPa)")
    print(f"☁️ Cloud Cover: {cloud} %")
    print("------------------------------")

    if 0 <= score <= 2.5:
        print(f"🔴 Fish activity is very weak, stay home!     {score} / 10")
    elif 2.5 < score <= 5:
        print(f"🟠 Fish activity is poor!     {score} / 10")
    elif 5 < score <= 7.5:
        print(f"🟢 Fish activity is good!     {score} / 10")
    elif 7.5 < score <= 10:
        print(f"🔵 Fish activity is excellent!     {score} / 10")