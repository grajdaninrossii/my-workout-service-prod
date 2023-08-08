import logging

# Настройка логов
logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', # настраиваем вывод (как и что будем выводить)
    # level = logging.INFO # уровень логов (все или только основные)
    level = logging.DEBUG # уровень логов (все или только основные)
)

logging.getLogger('sqlalchemy').setLevel(logging.ERROR)