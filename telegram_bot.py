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

traductor = GoogleTranslator(source="auto", target="es")
url_telegram = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# CONSULTAS ESPECIALES
query_iran = (
    "(Iran OR Iranian OR Tehran OR \"Iran conflict\" OR \"Israel Iran\" OR "
    "\"US Iran\" OR \"Middle East conflict\" OR \"Strait of Hormuz\")"
)

query_trump = (
    "(Trump OR \"Donald Trump\" OR \"Trump administration\" OR "
    "\"Trump policy\" OR \"Trump tariffs\" OR \"Trump election\")"
)

# CONSULTA GLOBAL + CRIPTO
query_global = (
    "(AI OR economy OR geopolitics OR war OR energy OR technology OR "
    "semiconductor OR inflation OR china OR russia OR markets OR "
    "bitcoin OR crypto OR cryptocurrency OR ethereum OR blockchain OR "
    "binance OR defi OR nft OR stablecoin OR altcoins OR web3 OR "
    "regulation OR etf OR tokenization)"
)

DOMINIOS = (
    "reuters.com,bbc.com,bloomberg.com,theverge.com,cnn.com,"
    "coindesk.com,cointelegraph.com,theblock.co"
)

def obtener_noticias(query, page_size=20):
    url_news = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&"
        f"domains={DOMINIOS}&"
        f"language=en&"
        f"sortBy=publishedAt&"
        f"pageSize={page_size}&"
        f"apiKey={NEWS_API_KEY}"
    )

    data = requests.get(url_news).json()

    if data.get("status") != "ok":
        print("Error al obtener noticias:")
        print(data)
        return []

    return data.get("articles", [])

def enviar_telegram(texto):
    response = requests.post(url_telegram, data={
        "chat_id": CHAT_ID,
        "text": texto[:3500],
        "parse_mode": "HTML"
    })

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    time.sleep(1)

def preparar_mensaje(art):
    titulo = art.get("title") or "Sin título"
    descripcion = art.get("description") or "Sin descripción disponible."
    link = art.get("url") or "Sin link"

    titulo_es = traductor.translate(titulo)
    descripcion_es = traductor.translate(descripcion)

    titulo_es = html.escape(titulo_es)
    descripcion_es = html.escape(descripcion_es)
    link = html.escape(link)

    mensaje = f"""<b>{titulo_es}</b>

{descripcion_es}

Link: {link}
"""
    return mensaje

def enviar_primera_noticia_disponible(articulos, enviados_en_esta_corrida):
    for art in articulos:
        link = art.get("url") or ""

        if not link:
            continue

        if link in noticias_enviadas:
            continue

        if link in enviados_en_esta_corrida:
            continue

        mensaje = preparar_mensaje(art)
        enviar_telegram(mensaje)

        noticias_enviadas.append(link)
        enviados_en_esta_corrida.add(link)

        return True

    return False

# OBTENER NOTICIAS
articulos_iran = obtener_noticias(query_iran, page_size=10)
articulos_trump = obtener_noticias(query_trump, page_size=10)
articulos_global = obtener_noticias(query_global, page_size=60)

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

enviados_en_esta_corrida = set()
contador = 0

# ENVIAR 1 NOTICIA DE IRÁN
if enviar_primera_noticia_disponible(articulos_iran, enviados_en_esta_corrida):
    contador += 1

# ENVIAR 1 NOTICIA DE DONALD TRUMP
if enviar_primera_noticia_disponible(articulos_trump, enviados_en_esta_corrida):
    contador += 1

# COMPLETAR HASTA 12 NOTICIAS CON GLOBALES + CRIPTO
for art in articulos_global:
    if contador >= 12:
        break

    link = art.get("url") or ""

    if not link:
        continue

    if link in noticias_enviadas:
        continue

    if link in enviados_en_esta_corrida:
        continue

    mensaje = preparar_mensaje(art)
    enviar_telegram(mensaje)

    noticias_enviadas.append(link)
    enviados_en_esta_corrida.add(link)

    contador += 1

# LIMITAR HISTORIAL
noticias_enviadas = noticias_enviadas[-300:]

# GUARDAR HISTORIAL
with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as f:
    json.dump(noticias_enviadas, f, ensure_ascii=False, indent=4)
