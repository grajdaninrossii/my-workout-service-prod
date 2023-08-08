from environs import Env
from fastapi.templating import Jinja2Templates

# Путь к шаблонам
templates = Jinja2Templates(directory="./fast_api_core/templates")

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
LIST_OF_ADMINS = env.str("ADMINS")
POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
POSTGRES_SERVER = env.str("POSTGRES_SERVER")
POSTGRES_DB = env.str("POSTGRES_DB")
NGROK_AUTHTOKEN = env.str("NGROK_AUTHTOKEN")