import os
import requests
from datetime import datetime

TOKEN = "8722291649:AAHoOAQBBpgd5FIAiTyhhnfhxhrgiGBLmpc"
CHAT_ID = "1054479634"
NEWS_API_KEY = "8ae3d3cc425f4956a20c5d8e4da703d4"

fecha_hoy = datetime.now().strftime("%d/%m/%Y")

url_news = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=5&apiKey={NEWS_API_KEY}"
data = requests.get(url_news).json()

articulos = data.get("articles", [])

mensaje = f"""GLOBAL NEWS DASHBOARD — TODAY

Fecha: {fecha_hoy}
Cobertura: últimas 24 horas

"""

for i, art in enumerate(articulos, start=1):
    titulo = art.get("title", "Sin título")
    link = art.get("url", "Sin link")

    mensaje += f"{i}. {titulo}\n"
    mensaje += f"Link: {link}\n\n"

# DIVIDIR MENSAJE EN PARTES
def dividir_mensaje(texto, limite=4000):
    partes = []
    while len(texto) > limite:
        partes.append(texto[:limite])
        texto = texto[limite:]
    partes.append(texto)
    return partes

partes = dividir_mensaje(mensaje)

for parte in partes:
    params = {
        "chat_id": CHAT_ID,
        "text": parte,
        "parse_mode": "Markdown"
    }

    telegram_response = requests.post(url_telegram, data=params)
    print("STATUS:", telegram_response.status_code)
    print("RESPONSE:", telegram_response.text)

url_telegram = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

params = {
    "chat_id": CHAT_ID,
    "text": mensaje
}

response = requests.post(url_telegram, data=params)

print("TELEGRAM STATUS:", response.status_code)
print("TELEGRAM RESPONSE:", response.text)
