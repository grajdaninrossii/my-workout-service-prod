from telegram.ext import ConversationHandler
from utils.navigation import (
    CHOICE_SETTINGS_KEY,
    SET_USER_DATA_KEY,
    SET_GENDER_KEY,
    SET_AGE_KEY,
    SET_HEIGHT_KEY,
    SET_WEIGHT_KEY,
    SET_GOAL_KEY,
    BACK_KEY,
    MAIN_MENU_KEY
)
from handlers.workout_handlers.test_workout_handlers import (
    back_2_main_menu_handler,
)
from handlers.user_handlers.user_settings_handlers import (
    # get_user_age_quiz_handler,
    user_settings_handler,
    set_gender_handler,
    set_age_handler,
    set_height_handler,
    set_weight_handler,
    set_goal_handler,
    support_handler,
    settings_handler,
    choice_user_setting_handler,
    back_to_setting_menu_handler,
    get_user_data_handler
)


# Настройки
conv_setting = ConversationHandler(
    entry_points=[settings_handler],
    states={
        CHOICE_SETTINGS_KEY: [user_settings_handler, support_handler, back_2_main_menu_handler],
        SET_USER_DATA_KEY: [choice_user_setting_handler, back_to_setting_menu_handler, get_user_data_handler],
        SET_GENDER_KEY: [set_gender_handler],
        SET_AGE_KEY: [set_age_handler],
        SET_HEIGHT_KEY: [set_height_handler],
        SET_WEIGHT_KEY: [set_weight_handler],
        SET_GOAL_KEY: [set_goal_handler],
    },
    fallbacks=[],
    map_to_parent={
        BACK_KEY: MAIN_MENU_KEY,
        MAIN_MENU_KEY: MAIN_MENU_KEY
    },
    name="setting_conversation",
    persistent = True,
)