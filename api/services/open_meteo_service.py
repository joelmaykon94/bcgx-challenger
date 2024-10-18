import requests

def get_weather_data(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()
    return data['hourly']['temperature_2m']

latitude = -23.5505  # Exemplo: São Paulo
longitude = -46.6333
weather_data = get_weather_data(latitude, longitude)

print(f"Temperatura atual em São Paulo: {weather_data[0]}°C")
