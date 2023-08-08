import asyncio
from typing import Generator
from config.logger import logging
from config.settings import NGROK_AUTHTOKEN
from pyngrok import ngrok

ngrok.set_auth_token(NGROK_AUTHTOKEN)
# Перекидываем порт в туннель (хз точно как)))
# tunnel = ngrok.connect(8000)
tunnel = ngrok.connect(8000)
public_url = tunnel.public_url
logging.debug(f"Мой url: {public_url}")

loop = asyncio.get_event_loop()

# def event_loop() -> Generator:
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()