from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from db.database import save_listing, listing_exists
from alerts.telegram_alert import send_telegram_alert
from config.settings import WORK_HOURS
from datetime import datetime
import time

# ✅ TODOS OS LINKS ORGANIZADOS POR IDENTIFICADOR
TARGETS = {
    "gaia-casas": "https://www.idealista.pt/comprar-casas/vila-nova-de-gaia/",
    "espinho-casas": "https://www.idealista.pt/comprar-casas/espinho/espinho/",
    "gondomar-casas": "https://www.idealista.pt/comprar-casas/gondomar/",
    "porto-armazens": "https://www.idealista.pt/geo/comprar-lojas_ou_armazens/area-metropolitana-do-porto/",
    "gaia-armazens": "https://www.idealista.pt/comprar-lojas_ou_armazens/vila-nova-de-gaia/",
    "gondomar-armazens": "https://www.idealista.pt/comprar-lojas_ou_armazens/gondomar/",
    "porto-predios": "https://www.idealista.pt/comprar-predios/porto/",
    "espinho-predios": "https://www.idealista.pt/comprar-predios/espinho/espinho/",
    "gondomar-predios": "https://www.idealista.pt/comprar-predios/gondomar/mapa"
}

def is_outside_work_hours():
    now = datetime.now().time()
    start = datetime.strptime(WORK_HOURS["start"], "%H:%M").time()
    end = datetime.strptime(WORK_HOURS["end"], "%H:%M").time()
    return now < start or now > end

def scrape_idealista_target(target_id):
    if target_id not in TARGETS:
        print(f"❌ Target inválido: {target_id}")
        return

    url = TARGETS[target_id]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()

        print(f"🔍 A procurar em: {target_id}")
        page.goto(url, timeout=60000)

        for _ in range(3):
            page.mouse.wheel(0, 1000)
            time.sleep(2)

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        listings = soup.select("article.item")
        print(f"📌 {len(listings)} anúncios encontrados em {target_id}")

        for item in listings[:10]:
            try:
                title_el = item.select_one("a.item-link")
                price_el = item.select_one("span.item-price")

                if not title_el or not price_el:
                    continue

                title = title_el.get_text(strip=True)
                price = price_el.get_text(strip=True)
                relative_url = title_el.get("href")
                full_url = "https://www.idealista.pt" + relative_url

                if not listing_exists(full_url):
                    save_listing(title, price, full_url)
                    out_of_hours = is_outside_work_hours()
                    send_telegram_alert(title, price, full_url, out_of_hours)
                    time.sleep(2)
                else:
                    print(f"🔁 Já existe: {title}")

            except Exception as e:
                print("❌ Erro ao processar anúncio:", e)

        browser.close()