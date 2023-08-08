from telegram.ext import ConversationHandler
from utils.navigation import (
    CHOICE_PROGRESS_KEY,
    BACK_KEY,
    MAIN_MENU_KEY
)
from handlers.workout_handlers.test_workout_handlers import (
    back_2_main_menu_handler,
)
from handlers.user_handlers.progress_handlers import (
    progress_graphic_handler,
    progress_handler,
)


# Прогресс
conv_progress = ConversationHandler(
    entry_points=[progress_handler],
    states={
        CHOICE_PROGRESS_KEY: [progress_graphic_handler, back_2_main_menu_handler]
    },
    fallbacks=[],
    map_to_parent={
        BACK_KEY: MAIN_MENU_KEY,
        MAIN_MENU_KEY: MAIN_MENU_KEY
    },
    name="progress_conversation",
    persistent = True,
)