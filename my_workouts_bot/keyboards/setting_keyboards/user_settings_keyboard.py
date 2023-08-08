from telegram import KeyboardButton, ReplyKeyboardMarkup

from keyboards.keyboard_buttons import UserSettingsButtons


user_settings_buttons_list = [
    KeyboardButton(UserSettingsButtons.gender),
    KeyboardButton(UserSettingsButtons.age),
    KeyboardButton(UserSettingsButtons.weight),
    KeyboardButton(UserSettingsButtons.height),
    KeyboardButton(UserSettingsButtons.goal),
    KeyboardButton(UserSettingsButtons.about_me),
    KeyboardButton(UserSettingsButtons.back)
]


user_settings_keyboard = ReplyKeyboardMarkup(
    [user_settings_buttons_list[:5], [user_settings_buttons_list[5]], [user_settings_buttons_list[6]]],
    resize_keyboard=True
)