import os
import time
import json
import html
import requests
from datetime import datetime
from deep_translator import GoogleTranslator

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

fecha_hoy = datetime.now().strftime("%d/%m/%Y")

ARCHIVO_HISTORIAL = "noticias_enviadas.json"

# CARGAR HISTORIAL
if os.path.exists(ARCHIVO_HISTORIAL):
    with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as f:
        noticias_enviadas = json.load(f)
else:
    noticias_enviadas = []

# CONSULTA GLOBAL + CRIPTO
query = (
    "(AI OR economy OR geopolitics OR war OR energy OR technology OR "
    "semiconductor OR inflation OR china OR russia OR markets OR "
    "bitcoin OR crypto OR cryptocurrency OR ethereum OR blockchain OR "
    "binance OR defi OR nft OR stablecoin OR altcoins OR web3 OR "
    "regulation OR etf OR tokenization)"
)

# OBTENER NOTICIAS
url_news = (
    f"https://newsapi.org/v2/everything?"
    f"q={query}&"
    f"domains=reuters.com,bbc.com,bloomberg.com,theverge.com,cnn.com,coindesk.com,cointelegraph.com,theblock.co&"
    f"language=en&"
    f"sortBy=publishedAt&"
    f"pageSize=60&"
    f"apiKey={NEWS_API_KEY}"
)

data = requests.get(url_news).json()

if data.get("status") != "ok":
    print("Error al obtener noticias:")
    print(data)
    exit()

articulos = data.get("articles", [])

traductor = GoogleTranslator(source="auto", target="es")

url_telegram = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# ENCABEZADO
intro = f"""<b>GLOBAL NEWS</b>

<b>{fecha_hoy}</b>
"""

requests.post(url_telegram, data={
    "chat_id": CHAT_ID,
    "text": intro,
    "parse_mode": "HTML"
})

time.sleep(1)

contador = 0

# PROCESAR NOTICIAS
for art in articulos:

    titulo = art.get("title") or "Sin título"
    descripcion = art.get("description") or "Sin descripción disponible."
    link = art.get("url") or "Sin link"

    noticia_id = link

    # EVITAR REPETIDAS
    if noticia_id in noticias_enviadas:
        continue

    titulo_es = traductor.translate(titulo)
    descripcion_es = traductor.translate(descripcion)

    titulo_es = html.escape(titulo_es)
    descripcion_es = html.escape(descripcion_es)
    link = html.escape(link)

    mensaje = f"""{contador + 1}. <b>{titulo_es}</b>

{descripcion_es}

Link: {link}
"""

    response = requests.post(url_telegram, data={
        "chat_id": CHAT_ID,
        "text": mensaje[:3500],
        "parse_mode": "HTML"
    })

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    # GUARDAR COMO ENVIADA
    noticias_enviadas.append(noticia_id)

    contador += 1

    time.sleep(1)

    # LIMITAR A 12 NOTICIAS
    if contador >= 12:
        break

# LIMITAR HISTORIAL
noticias_enviadas = noticias_enviadas[-300:]

# GUARDAR HISTORIAL
with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as f:
    json.dump(noticias_enviadas, f, ensure_ascii=False, indent=4)
