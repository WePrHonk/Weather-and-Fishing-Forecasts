# Weather and Fishing Forecasts

A Python application that uses weather data from Open-Meteo API to analyze fishing conditions and calculate fishing activity score.

## Features

- Get weather data using Open-Meteo API
- Analyze fishing conditions based on weather factors
- Calculate fishing activity score from 0 to 10
- Analyze:
  - Temperature
  - Wind speed
  - Wind direction
  - Air pressure changes
  - Cloud cover
  - Time of day
- Search weather by city name

## Technologies

- Python 3
- Requests
- Open-Meteo API
- JSON

## Installation

1. Clone the repository:

```bash
git clone https://github.com/WePrHonk/Weather-and-Fishing-Forecasts.git
```

2. Install the required library:

```bash
pip install -r requirements.txt
```

3. Run the program:

```bash
python main.py
```

## Usage

1. Run the program.
2. Enter the city name.
3. Enter the desired hour (0–23).
4. Receive the weather forecast and fishing activity score for the selected city and hour.

## Example

Example Output:

```text
City: London
Coordinates: 51.50853, -0.12574
Hour: 21:00
--------------------------------
Temperature: 24.0°C
Wind Speed: 6.8 m/s  (24.5 km/h)
Wind Direction: 344°
Precipitation: 0.0 mm
Pressure: 762.1 mmHg  (1016.1 hPa)
Cloud Cover: 88%
--------------------------------
Fishing activity is excellent!     7.1/10
```

## Screenshot
Example of program output:
![Fishing forecast example](screenshots/fishing_forecast_example.png)

## Future Improvements

- Add weather forecast for multiple days
- Improve fishing activity calculation algorithm
- Add data visualization with charts
- Add error handling for API requests
- Create automated tests using pytest
- Add graphical user interface (GUI)