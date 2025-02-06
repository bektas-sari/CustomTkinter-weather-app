import customtkinter as ctk
import requests
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# API Anahtarını al
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Hava durumu ikonları
WEATHER_ICONS = {
    "clear sky": "☀️",
    "few clouds": "🌤️",
    "scattered clouds": "⛅",
    "broken clouds": "☁️",
    "shower rain": "🌦️",
    "rain": "🌧️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️"
}

def get_weather():
    """ Kullanıcının girdiği şehir için hava durumu bilgisini getirir. """
    city = city_entry.get()
    if not city:
        result_label.configure(text="❌ Please enter a city name", text_color="red")
        return

    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric",
            "lang": "en"
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        data = response.json()
        city_name = data["name"]
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"].lower()
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # Hava durumu açıklamasına göre ikon seç
        weather_icon = WEATHER_ICONS.get(weather_desc, "🌍")

        # Sonuçları göstermek için yeni bir çerçeve oluştur
        result_frame.pack(pady=15, padx=20, fill="x")

        # Şehir adı
        city_label.configure(text=f"{weather_icon} {city_name}")

        # **Bilgileri Güncelle (Yarım TAB boşluk için padx=10 kullanıyoruz)**
        temp_icon.configure(text="🌡️")
        temp_label.configure(text=f"Temperature: {temp}°C")

        condition_icon.configure(text="🌦️")
        condition_label.configure(text=f"Condition: {weather_desc.capitalize()}")

        wind_icon.configure(text="💨")
        wind_label.configure(text=f"Wind: {wind_speed} m/s")

        humidity_icon.configure(text="💧")
        humidity_label.configure(text=f"Humidity: {humidity}%")

        # Genel sonuç etiketi
        result_label.configure(text="✅ Data Retrieved Successfully!", text_color="green")

    except requests.exceptions.RequestException:
        result_label.configure(text="❌ City not found or API error!", text_color="red")


# **Arayüzü oluştur**
ctk.set_appearance_mode("light")  # Açık mod
ctk.set_default_color_theme("blue")  # Mavi tema

app = ctk.CTk()
app.title("Weather App")
app.geometry("500x550")  # Daha geniş bir pencere
app.resizable(False, False)

# **Arkaplan rengi (açık renk)**
app.configure(bg="#F9F9F9")

# **Başlık etiketi**
title_label = ctk.CTkLabel(app, text="🌦️ Weather App", font=("Helvetica", 26, "bold"), text_color="darkblue", bg_color="transparent")
title_label.pack(pady=20)

# **Şehir giriş kutusu (Daha büyük ve belirgin hale getirildi)**
city_entry = ctk.CTkEntry(app, placeholder_text="Enter city name", font=("Helvetica", 18), width=340, height=45, corner_radius=12, fg_color="white", text_color="black")
city_entry.pack(pady=10)

# **Hava durumu sorgulama butonu**
search_button = ctk.CTkButton(app, text="Get Weather", command=get_weather, font=("Helvetica", 18, "bold"), width=220, height=45, corner_radius=12, fg_color="blue", hover_color="#0059ff")
search_button.pack(pady=15)

# **Sonuçlar için Çerçeve (Yarım TAB Boşluk için padx=10)**
result_frame = ctk.CTkFrame(app, fg_color="white", corner_radius=12)
result_frame.pack(pady=15, padx=20, fill="x")

city_label = ctk.CTkLabel(result_frame, text="", font=("Helvetica", 22, "bold"), text_color="black")
city_label.pack(pady=10)

# **Bilgi Satırlarını Tek Tek Oluştur (İkonlar ve Metinler Arasında Yarım TAB Boşluk)**
info_frame = ctk.CTkFrame(result_frame, fg_color="white")
info_frame.pack(anchor="w", padx=20, pady=5)

temp_icon = ctk.CTkLabel(info_frame, text="", font=("Helvetica", 18))
temp_icon.grid(row=0, column=0, sticky="w", padx=5)  # Yarım TAB boşluk için padx=5
temp_label = ctk.CTkLabel(info_frame, text="", font=("Helvetica", 18), anchor="w")
temp_label.grid(row=0, column=1, sticky="w", padx=10)  # Yarım TAB boşluk için padx=10

condition_icon = ctk.CTkLabel(info_frame, text="", font=("Helvetica", 18))
condition_icon.grid(row=1, column=0, sticky="w", padx=5)
condition_label = ctk.CTkLabel(info_frame, text="", font=("Helvetica", 18), anchor="w")
condition_label.grid(row=1, column=1, sticky="w", padx=10)

wind_icon = ctk.CTkLabel(info_frame, text="", font=("Helvetica", 18))
wind_icon.grid(row=2, column=0, sticky="w", padx=5)
wind_label = ctk.CTkLabel(info_frame, text="", font=("Helvetica", 18), anchor="w")
wind_label.grid(row=2, column=1, sticky="w", padx=10)

humidity_icon = ctk.CTkLabel(info_frame, text="", font=("Helvetica", 18))
humidity_icon.grid(row=3, column=0, sticky="w", padx=5)
humidity_label = ctk.CTkLabel(info_frame, text="", font=("Helvetica", 18), anchor="w")
humidity_label.grid(row=3, column=1, sticky="w", padx=10)

# **Genel sonuç etiketi**
result_label = ctk.CTkLabel(app, text="", font=("Helvetica", 14), text_color="black", bg_color="transparent")
result_label.pack(pady=10)

# **Copyright Bilgisi (Küçük ve daha modern bir font ile)**
copyright_label = ctk.CTkLabel(app, text="@2025 - Bektas", font=("Helvetica", 10), text_color="gray", bg_color="transparent")
copyright_label.pack(pady=5)

app.mainloop()
