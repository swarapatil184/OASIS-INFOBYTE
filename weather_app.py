"""
Basic Weather App - Python Project 4 (Beginner Level)
=====================================================
This app fetches current weather data for a user-specified location
using the Open-Meteo API (free, no API key required!).

Displays: Temperature, Humidity, Wind Speed, and Weather Conditions
"""

import urllib.request
import urllib.parse
import json


# --- Weather condition codes from Open-Meteo ---
def get_weather_description(code):
    conditions = {
        0: "Clear sky ☀️",
        1: "Mainly clear 🌤️",
        2: "Partly cloudy ⛅",
        3: "Overcast ☁️",
        45: "Foggy 🌫️",
        48: "Icy fog 🌫️",
        51: "Light drizzle 🌦️",
        53: "Moderate drizzle 🌦️",
        55: "Dense drizzle 🌧️",
        61: "Slight rain 🌧️",
        63: "Moderate rain 🌧️",
        65: "Heavy rain 🌧️",
        71: "Slight snow 🌨️",
        73: "Moderate snow 🌨️",
        75: "Heavy snow ❄️",
        80: "Slight rain showers 🌦️",
        81: "Moderate rain showers 🌧️",
        82: "Violent rain showers ⛈️",
        95: "Thunderstorm ⛈️",
        99: "Thunderstorm with hail ⛈️",
    }
    return conditions.get(code, "Unknown condition")


# --- Step 1: Get coordinates from city name ---
def get_coordinates(city_name):
    print(f"\n🔍 Searching for '{city_name}'...")
    
    encoded_city = urllib.parse.quote(city_name)
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_city}&count=1"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        if "results" not in data or len(data["results"]) == 0:
            print(f"❌ City '{city_name}' not found. Please check the spelling.")
            return None
        
        result = data["results"][0]
        return {
            "name": result["name"],
            "country": result.get("country", ""),
            "latitude": result["latitude"],
            "longitude": result["longitude"]
        }
    
    except Exception as e:
        print(f"❌ Error finding city: {e}")
        return None


# --- Step 2: Fetch weather data ---
def get_weather(latitude, longitude):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m,relative_humidity_2m,"
        f"wind_speed_10m,weathercode"
        f"&temperature_unit=celsius"
    )
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
        return data["current"]
    
    except Exception as e:
        print(f"❌ Error fetching weather: {e}")
        return None


# --- Step 3: Display the weather ---
def display_weather(location, weather):
    print("\n" + "=" * 45)
    print(f"  🌍 Weather for {location['name']}, {location['country']}")
    print("=" * 45)
    
    condition = get_weather_description(weather["weathercode"])
    temp = weather["temperature_2m"]
    humidity = weather["relative_humidity_2m"]
    wind = weather["wind_speed_10m"]
    
    print(f"  Condition   : {condition}")
    print(f"  Temperature : {temp}°C  ({round(temp * 9/5 + 32, 1)}°F)")
    print(f"  Humidity    : {humidity}%")
    print(f"  Wind Speed  : {wind} km/h")
    print("=" * 45)
    
    # Simple advice based on conditions
    if temp < 10:
        print("  💡 Tip: It's cold outside — wear a jacket!")
    elif temp > 35:
        print("  💡 Tip: Very hot! Stay hydrated and use sunscreen.")
    
    if humidity > 80:
        print("  💡 Tip: High humidity — might feel sticky outside.")
    
    if wind > 40:
        print("  💡 Tip: Strong winds — hold onto your hat! 🎩")
    
    print()


# --- Main Program ---
def main():
    print("=" * 45)
    print("   🌤️  Basic Weather App  🌤️")
    print("   Python Programming - Project 4")
    print("=" * 45)
    
    while True:
        print("\nOptions:")
        print("  1. Check weather for a city")
        print("  2. Exit")
        
        choice = input("\nEnter your choice (1 or 2): ").strip()
        
        if choice == "2":
            print("\n👋 Goodbye! Stay weather-aware!")
            break
        
        elif choice == "1":
            city = input("Enter city name (e.g., Mumbai, London, New York): ").strip()
            
            if not city:
                print("❌ Please enter a valid city name.")
                continue
            
            # Get coordinates
            location = get_coordinates(city)
            if location is None:
                continue
            
            # Get weather
            weather = get_weather(location["latitude"], location["longitude"])
            if weather is None:
                continue
            
            # Display results
            display_weather(location, weather)
        
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")


# Run the program
if __name__ == "__main__":
    main()
