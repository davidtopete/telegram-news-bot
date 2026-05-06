import requests
from datetime import datetime
from deep_translator import GoogleTranslator

# 🔹 CONFIG
TOKEN = "8722291649:AAHoOAQBBpgd5FIAiTyhhnfhxhrgiGBLmpc"
CHAT_ID = "1054479634"
NEWS_API_KEY = "8ae3d3cc425f4956a20c5d8e4da703d4"

# FECHA
fecha_hoy = datetime.now().strftime("%d/%m/%Y")

# OBTENER NOTICIAS EN INGLÉS
url_news = (
    f"https://newsapi.org/v2/top-headlines?"
    f"language=en&pageSize=10&apiKey={NEWS_API_KEY}"
)

response = requests.get(url_news)
data = response.json()

if data.get("status") != "ok":
    print("Error al obtener noticias:")
    print(data)
    exit()

articulos = data.get("articles", [])

# CREAR MENSAJE
mensaje = "**GLOBAL NEWS DASHBOARD — TODAY**\n\n"
mensaje += f"**Fecha: {fecha_hoy}**\n"
mensaje += "**Cobertura: últimas 24 horas**\n\n"

traductor = GoogleTranslator(source="auto", target="es")

for i, art in enumerate(articulos, start=1):
    titulo = art.get("title") or "Sin título"
    descripcion = art.get("description") or "Sin descripción disponible."
    link = art.get("url") or "Sin link"

    # TRADUCIR A ESPAÑOL
    titulo_es = traductor.translate(titulo)
    descripcion_es = traductor.translate(descripcion)

    mensaje += f"{i}. **{titulo_es}**\n"
    mensaje += f"   Fecha: {fecha_hoy}\n"
    mensaje += f"   {descripcion_es}\n"
    mensaje += f"   Link: {link}\n\n"

# ENVIAR A TELEGRAM
url_telegram = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

params = {
    "chat_id": CHAT_ID,
    "text": mensaje,
    "parse_mode": "Markdown"
}

telegram_response = requests.post(url_telegram, data=params)

print(telegram_response.json())