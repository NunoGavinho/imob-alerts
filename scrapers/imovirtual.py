from playwright.sync_api import sync_playwright
from db.database import save_listing, listing_exists
from alerts.telegram_alert import send_telegram_alert
from config.settings import SEARCH_URL, WORK_HOURS
from datetime import datetime
import time

def is_outside_work_hours():
    """Verifica se está fora do horário configurado"""
    now = datetime.now().time()
    start = datetime.strptime(WORK_HOURS["start"], "%H:%M").time()
    end = datetime.strptime(WORK_HOURS["end"], "%H:%M").time()
    return now < start or now > end

def scrape_imovirtual():
    """Faz scraping do Imovirtual, guarda novos e envia alertas"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(SEARCH_URL)
        page.wait_for_timeout(5000)  # Espera 5s para carregar tudo

        listings = page.query_selector_all("article[data-cy='listing-item']")

        for listing in listings[:5]:  # Primeiro 5 anúncios (testes)
            try:
                title = listing.query_selector("h2").inner_text().strip()
                link = listing.query_selector("a").get_attribute("href")
                full_link = "https://www.imovirtual.com" + link if link.startswith("/") else link
                price = listing.query_selector("p.price").inner_text().strip()

                if not listing_exists(full_link):
                    save_listing(title, price, full_link)
                    out_of_hours = is_outside_work_hours()
                    send_telegram_alert(title, price, full_link, out_of_hours)
                    time.sleep(2)  # Evita parecer bot
                else:
                    print("🔁 Já existente:", title)

            except Exception as e:
                print("❌ Erro ao processar anúncio:", e)

        browser.close()
