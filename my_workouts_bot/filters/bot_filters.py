from telegram.ext import filters
from keyboards.keyboard_buttons import (
    BACK_BUTTON_TEXT,
    SelectFoodButtons,
    MainMenuButtons
    )

# Для установки данных (любые текстовые сообщения, кроме общих команд)
set_data_filter = filters.TEXT & ~filters.COMMAND
set_data_with_back_filter = filters.TEXT & ~filters.COMMAND & ~filters.Regex(f'Назад')

# для обработки ошибочного ввода
all_message_filter = filters.TEXT | filters.PHOTO | filters.VIDEO | filters.VOICE

# Кнока назад
back_filter = filters.Regex(BACK_BUTTON_TEXT)

# Выбор типа меню
select_food_filter = filters.Regex(MainMenuButtons.food)
get_day_ration_filter = filters.Regex(SelectFoodButtons.day)
get_one_ration_filter = filters.Regex(SelectFoodButtons.breakfast) | \
filters.Regex(SelectFoodButtons.bite) | \
filters.Regex(SelectFoodButtons.lunch) | \
filters.Regex(SelectFoodButtons.snack) | \
filters.Regex(SelectFoodButtons.dinner) | \
filters.Regex(SelectFoodButtons.before_sleep)