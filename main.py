import sys
from db.database import init_db
from scrapers.idealista import scrape_idealista_target

if __name__ == "__main__":
    init_db()

    if len(sys.argv) != 2:
        print("❗ Uso correto: python main.py <target_id>")
        print("Exemplo: python main.py gaia-casas")
        sys.exit(1)

    target_id = sys.argv[1]
    scrape_idealista_target(target_id)
