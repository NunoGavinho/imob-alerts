import sqlite3
import os

# Caminho para o ficheiro de base de dados
DB_PATH = os.path.join(os.path.dirname(__file__), "listings.db")

def init_db():
    """Cria a tabela se ainda não existir"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price TEXT,
            link TEXT UNIQUE,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_listing(title, price, link):
    """Guarda um novo anúncio na base de dados"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO listings (title, price, link) VALUES (?, ?, ?)", (title, price, link))
    conn.commit()
    conn.close()

def listing_exists(link):
    """Verifica se o anúncio já foi guardado"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM listings WHERE link = ?", (link,))
    result = c.fetchone()
    conn.close()
    return result is not None
