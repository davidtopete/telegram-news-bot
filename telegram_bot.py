import os
import requests
from datetime import datetime

TOKEN = os.getenv("8722291649:AAHoOAQBBpgd5FIAiTyhhnfhxhrgiGBLmpc")
CHAT_ID = os.getenv("1054479634")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

fecha_hoy = datetime.now().strftime("%d/%m/%Y")

url_news = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=10&apiKey={NEWS_API_KEY}"
data = requests.get(url_news).json()

articulos = data.get("articles", [])

url_telegram = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# Mensaje inicial
intro = f"""GLOBAL NEWS DASHBOARD — TODAY

Fecha: {fecha_hoy}
Cobertura: últimas 24 horas
"""

requests.post(url_telegram, data={
    "chat_id": CHAT_ID,
    "text": intro
})

# Enviar una noticia por mensaje
for i, art in enumerate(articulos, start=1):
    titulo = art.get("title", "Sin título")
    descripcion = art.get("description", "Sin descripción disponible.")
    link = art.get("url", "Sin link")

    mensaje = f"""{i}. {titulo}

Fecha: {fecha_hoy}
{descripcion}

Link: {link}
"""

    response = requests.post(url_telegram, data={
        "chat_id": CHAT_ID,
        "text": mensaje[:3500]
    })

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)
