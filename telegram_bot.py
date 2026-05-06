import os
import requests

TOKEN = os.getenv("8722291649:AAHoOAQBBpgd5FIAiTyhhnfhxhrgiGBLmpc")
CHAT_ID = os.getenv("1054479634")

url_telegram = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

params = {
    "chat_id": CHAT_ID,
    "text": "Hola"
}

response = requests.post(url_telegram, data=params)

print("STATUS:", response.status_code)
print("RESPONSE:", response.text)
