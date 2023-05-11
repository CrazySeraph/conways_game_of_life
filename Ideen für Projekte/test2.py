import tkinter as tk
import requests
import json


class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title("Weather App")

        self.label = tk.Label(master, text="Enter a city name:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.button = tk.Button(master, text="Get Weather", command=self.get_weather)
        self.button.pack()

        self.result = tk.Label(master, text="")
        self.result.pack()

    def get_weather(self):
        city = self.entry.get()
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=0a3e9a7f23d9c6a7f9205e5eb5b5e5b5"
        response = requests.get(url)
        data = json.loads(response.text)
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        temp_f = (temp - 273.15) * 9 / 5 + 32
        self.result.config(text=f"The weather in {city} is {weather}. The temperature is {temp_f:.2f} °F.")


root = tk.Tk()
app = WeatherApp(root)
root.mainloop()