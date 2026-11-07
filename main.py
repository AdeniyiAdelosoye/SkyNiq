
import requests
import tkinter as tk
from tkinter import messagebox
import threading


BACKGROUND = "#E8F5EE"
MAIN_GREEN = "#167D70"
DETAIL_GREEN = "#269B87"
HEADING_GREEN = "#075E59"
SUNSHINE_YELLOW = "#FFC857"
BUTTON_HOVER = "#E9B447"
LIGHT_TEXT = "#E3FFF2"
SUBTITLE_COLOUR = "#628575"
ERROR_COLOUR = "#FFB4A2"
DIVIDER_COLOUR = "#80C9B3"


def find_city(city_name):
    url = "https://geocoding-api.open-meteo.com/v1/search"

    parameters = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(
            url,
            params=parameters,
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            print("City not found.")
            return None

        city = data["results"][0]

        print("City:", city["name"])
        print("Country:", city["country"])
        print("Latitude:", city["latitude"])
        print("Longitude:", city["longitude"])

        return city

    except requests.exceptions.RequestException as error:
        print("Connection error:", error)
        return None

    except (ValueError, KeyError) as error:
        print("Invalid city data:", error)
        return None


def get_weather_description(code):
    descriptions = {
        0: "Clear Sky",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing Rime Fog",
        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",
        56: "Light Freezing Drizzle",
        57: "Dense Freezing Drizzle",
        61: "Slight Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        66: "Light Freezing Rain",
        67: "Heavy Freezing Rain",
        71: "Slight Snowfall",
        73: "Moderate Snowfall",
        75: "Heavy Snowfall",
        77: "Snow Grains",
        80: "Slight Rain Showers",
        81: "Moderate Rain Showers",
        82: "Violent Rain Showers",
        85: "Slight Snow Showers",
        86: "Heavy Snow Showers",
        95: "Thunderstorm",
        96: "Thunderstorm with Slight Hail",
        99: "Thunderstorm with Heavy Hail"
    }

    return descriptions.get(
        code,
        "Unknown Weather Condition"
    )


def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"

    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "weather_code"
        ),
        "wind_speed_unit": "kmh",
        "timezone": "auto"
    }

    try:
        response = requests.get(
            url,
            params=parameters,
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        weather = data["current"]

        required_fields = [
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m",
            "weather_code"
        ]

        if any(
            weather.get(field) is None
            for field in required_fields
        ):
            print("Incomplete weather data.")
            return None

        print("\nCurrent Weather")

        print(
            f"Temperature: "
            f"{weather['temperature_2m']}°C"
        )

        print(
            f"Humidity: "
            f"{weather['relative_humidity_2m']}%"
        )

        print(
            f"Wind Speed: "
            f"{weather['wind_speed_10m']} km/h"
        )

        print(
            "Weather Condition:",
            get_weather_description(
                weather["weather_code"]
            )
        )

        return weather

    except requests.exceptions.RequestException as error:
        print("Weather API error:", error)
        return None

    except (KeyError, ValueError, TypeError) as error:
        print("Invalid weather data:", error)
        return None


def display_weather(city, weather):
    description = get_weather_description(
        weather["weather_code"]
    )

    city_label.config(
        text=f"{city['name']}, {city['country']}",
        fg=LIGHT_TEXT
    )

    temperature_label.config(
        text=f"{weather['temperature_2m']}°C"
    )

    condition_label.config(
        text=description
    )

    humidity_value.config(
        text=f"{weather['relative_humidity_2m']}%"
    )

    wind_value.config(
        text=f"{weather['wind_speed_10m']} km/h"
    )

    search_button.config(
        state="normal",
        text="Get Weather"
    )


def display_error(message):
    city_label.config(
        text=message,
        fg=ERROR_COLOUR
    )

    temperature_label.config(text="--°C")
    condition_label.config(text="")
    humidity_value.config(text="--")
    wind_value.config(text="--")

    search_button.config(
        state="normal",
        text="Get Weather"
    )


def weather_worker(city_name):
    city = find_city(city_name)

    if city is None:
        root.after(
            0,
            lambda: display_error(
                "City not found or connection failed."
            )
        )
        return

    weather = get_weather(
        city["latitude"],
        city["longitude"]
    )

    if weather is None:
        root.after(
            0,
            lambda: display_error(
                "Unable to retrieve weather information."
            )
        )
        return

    root.after(
        0,
        lambda: display_weather(city, weather)
    )


def search_weather():
    if search_button["state"] == "disabled":
        return

    city_name = city_entry.get().strip()

    if not city_name:
        messagebox.showwarning(
            "Missing City",
            "Please enter a city name."
        )
        return

    city_label.config(
        text="Loading weather...",
        fg=LIGHT_TEXT
    )

    temperature_label.config(text="")
    condition_label.config(text="")
    humidity_value.config(text="--")
    wind_value.config(text="--")

    search_button.config(
        state="disabled",
        text="Searching..."
    )

    thread = threading.Thread(
        target=weather_worker,
        args=(city_name,),
        daemon=True
    )

    thread.start()


root = tk.Tk()

root.title("SkyNiq — Weather Information")
root.geometry("560x650")
root.configure(bg=BACKGROUND)
root.resizable(False, False)


title_label = tk.Label(
    root,
    text="☀ SkyNiq",
    font=("Arial", 22, "bold"),
    fg=HEADING_GREEN,
    bg=BACKGROUND
)

title_label.pack(pady=(25, 3))


subtitle_label = tk.Label(
    root,
    text="Live weather for cities worldwide",
    font=("Arial", 11),
    fg=SUBTITLE_COLOUR,
    bg=BACKGROUND
)

subtitle_label.pack(pady=(0, 20))


city_entry = tk.Entry(
    root,
    font=("Arial", 15),
    width=30,
    justify="center",
    relief="flat",
    bg="white",
    fg=HEADING_GREEN,
    insertbackground=HEADING_GREEN
)

city_entry.pack(
    ipady=12,
    pady=(0, 15)
)

city_entry.bind(
    "<Return>",
    lambda event: search_weather()
)


search_button = tk.Button(
    root,
    text="Get Weather",
    font=("Arial", 13, "bold"),
    command=search_weather,
    bg=SUNSHINE_YELLOW,
    fg=HEADING_GREEN,
    activebackground=BUTTON_HOVER,
    activeforeground=HEADING_GREEN,
    disabledforeground="#777777",
    relief="flat",
    padx=45,
    pady=12,
    cursor="hand2"
)

search_button.pack(pady=(0, 20))


weather_card = tk.Frame(
    root,
    bg=MAIN_GREEN,
    padx=20,
    pady=25
)

weather_card.pack(
    fill="x",
    padx=25
)


city_label = tk.Label(
    weather_card,
    text="Search for a city",
    font=("Arial", 15, "bold"),
    fg=LIGHT_TEXT,
    bg=MAIN_GREEN
)

city_label.pack(pady=(0, 12))


temperature_label = tk.Label(
    weather_card,
    text="--°C",
    font=("Arial", 38, "bold"),
    fg="white",
    bg=MAIN_GREEN
)

temperature_label.pack()


condition_label = tk.Label(
    weather_card,
    text="Weather information will appear here",
    font=("Arial", 14),
    fg=SUNSHINE_YELLOW,
    bg=MAIN_GREEN
)

condition_label.pack(pady=(5, 20))


divider = tk.Frame(
    weather_card,
    bg=DIVIDER_COLOUR,
    height=1
)

divider.pack(
    fill="x",
    pady=(0, 20)
)


details_frame = tk.Frame(
    weather_card,
    bg=MAIN_GREEN
)

details_frame.pack(fill="x")


humidity_card = tk.Frame(
    details_frame,
    bg=DETAIL_GREEN,
    padx=15,
    pady=18
)

humidity_card.pack(
    side="left",
    expand=True,
    fill="both",
    padx=(0, 5)
)


humidity_title = tk.Label(
    humidity_card,
    text="💧 Humidity",
    font=("Arial", 12),
    fg=LIGHT_TEXT,
    bg=DETAIL_GREEN
)

humidity_title.pack()


humidity_value = tk.Label(
    humidity_card,
    text="--",
    font=("Arial", 19, "bold"),
    fg="white",
    bg=DETAIL_GREEN
)

humidity_value.pack(pady=(8, 0))


wind_card = tk.Frame(
    details_frame,
    bg=DETAIL_GREEN,
    padx=15,
    pady=18
)

wind_card.pack(
    side="left",
    expand=True,
    fill="both",
    padx=(5, 0)
)


wind_title = tk.Label(
    wind_card,
    text="💨 Wind Speed",
    font=("Arial", 12),
    fg=LIGHT_TEXT,
    bg=DETAIL_GREEN
)

wind_title.pack()


wind_value = tk.Label(
    wind_card,
    text="--",
    font=("Arial", 19, "bold"),
    fg="white",
    bg=DETAIL_GREEN
)

wind_value.pack(pady=(8, 0))


root.mainloop()
