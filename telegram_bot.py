import os
import time
import requests
from datetime import datetime
from deep_translator import GoogleTranslator

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

fecha_hoy = datetime.now().strftime("%d/%m/%Y")

url_news = (
    f"https://newsapi.org/v2/top-headlines?"
    f"language=en&pageSize=10&apiKey={NEWS_API_KEY}"
)

data = requests.get(url_news).json()

if data.get("status") != "ok":
    print("Error al obtener noticias:")
    print(data)
    exit()

articulos = data.get("articles", [])
traductor = GoogleTranslator(source="auto", target="es")

url_telegram = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

intro = f"""GLOBAL NEWS DASHBOARD — TODAY

Fecha: {fecha_hoy}
Cobertura: últimas 24 horas
"""

requests.post(url_telegram, data={
    "chat_id": CHAT_ID,
    "text": intro
})

time.sleep(1)

for i, art in enumerate(articulos, start=1):
    titulo = art.get("title") or "Sin título"
    descripcion = art.get("description") or "Sin descripción disponible."
    link = art.get("url") or "Sin link"

    titulo_es = traductor.translate(titulo)
    descripcion_es = traductor.translate(descripcion)

    mensaje = f"""{i}. {titulo_es}

Fecha: {fecha_hoy}
{descripcion_es}

Link: {link}
"""

    response = requests.post(url_telegram, data={
        "chat_id": CHAT_ID,
        "text": mensaje[:3500]
    })

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    time.sleep(1)
