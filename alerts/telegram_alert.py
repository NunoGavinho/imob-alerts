import requests
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_alert(title, price, link, out_of_hours=False):
    prefix = "🕗 [Fora do horário] " if out_of_hours else "🏠 Novo imóvel!"
    message = f"{prefix}\n• {title}\n• {price}\n• [Ver anúncio]({link})"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("✅ Alerta enviado com sucesso!")
    except Exception as e:
        print("❌ Erro ao enviar alerta:", e)
