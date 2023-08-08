from telegram.ext import ConversationHandler
from handlers.food_handlers.food_handlers import (
    get_day_ration_handler,
    get_one_ration_handler,
    select_food_handler
)
from handlers.workout_handlers.test_workout_handlers import (
    back_2_main_menu_handler
)
from handlers.general_handlers import (
    encorrect_msg_main_handler
)

from utils.navigation import (
    CHOICE_FOOD_KEY,
    BACK_KEY,
    MAIN_MENU_KEY
)


# Выбор рациона питания
conv_food = ConversationHandler(
    entry_points=[select_food_handler],
    states={
        # ADD_USER_TRAIN: [conv_add_user_train], Вписать все в choice_train_key
        CHOICE_FOOD_KEY: [
            get_day_ration_handler,
            get_one_ration_handler,
            back_2_main_menu_handler,
            encorrect_msg_main_handler
        ],
    },
    fallbacks=[],
    map_to_parent={
        BACK_KEY: MAIN_MENU_KEY,
        MAIN_MENU_KEY: MAIN_MENU_KEY
    },
    name="food_conversation",
    persistent = True,
)