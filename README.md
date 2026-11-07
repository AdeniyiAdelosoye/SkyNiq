# ☀️ SkyNiq
### Your Sky. Your Weather.

**SkyNiq** is a Python desktop weather application that provides current weather information for cities around the world through a clean, interactive graphical interface.

Built using Python, Tkinter, and the Open-Meteo API, SkyNiq makes it easy to check temperature, weather conditions, humidity, and wind speed.

Developed by **Adeniyi Adelosoye** as part of the Python Development Internship at **Auspify Technologies**.

## ✨ Features

- **Global City Search** — Search for weather conditions in cities worldwide.
- **Current Temperature** — View temperatures in degrees Celsius (°C).
- **Weather Conditions** — Understand current conditions through readable weather descriptions.
- **Humidity Tracking** — View relative humidity percentages.
- **Wind Speed** — Check wind speeds in kilometres per hour.
- **Error Handling** — Receive helpful feedback for invalid city names, connection failures, and unavailable weather information.
- **Modern Interface** — A green-and-yellow Tkinter interface designed for simplicity and readability.

## 🛠️ Technologies Used

- Python 3
- Tkinter — Desktop graphical interface
- Requests — HTTP API communication
- JSON — Weather data processing
- Open-Meteo — Geocoding and current weather data

## 🚀 Getting Started

### Prerequisites

- Python 3 with Tkinter support
- An internet connection

### Installation

1. Clone the repository:

```bash
git clone https://github.com/AdeniyiAdelosoye/SkyNiq.git
```

2. Navigate into the project directory:

```bash
cd SkyNiq
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python main.py
```

## 📖 How to Use

1. Launch SkyNiq.
2. Enter a city name in the search field.
3. Click the search button or press Enter.
4. View the current weather information.
5. Search another city whenever needed.

## 🌐 Weather Data

SkyNiq uses the [Open-Meteo API](https://open-meteo.com/) to retrieve weather information.

The Geocoding API converts city names into coordinates, while the Forecast API provides current weather conditions.

Weather readings may differ slightly from other services because of differences in weather models, observation sources, and update times.

## 📁 Project Structure

```text
SkyNiq/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 👨‍💻 Developer

**Adeniyi Adelosoye**

- GitHub: https://github.com/AdeniyiAdelosoye
- LinkedIn: https://www.linkedin.com/in/adeniyi-adelosoye-9990b7315

## 🙏 Acknowledgements

Weather information provided by [Open-Meteo](https://open-meteo.com/).

Created as part of the Auspify Technologies Python Development Internship.

---

**SkyNiq — Your Sky. Your Weather.**