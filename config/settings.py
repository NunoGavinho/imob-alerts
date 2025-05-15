import yaml
import os

# Caminho para o ficheiro de configuração
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'settings.yaml')

# Carrega o YAML com segurança
with open(CONFIG_PATH, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

TELEGRAM_BOT_TOKEN = config['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = config['TELEGRAM_CHAT_ID']
SEARCH_URL = config['SEARCH_URL']
WORK_HOURS = config['WORK_HOURS']