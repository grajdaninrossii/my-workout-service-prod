def build_keyboard_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i  in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


# from telegram import KeyboardButton, ReplyKeyboardMarkup
# # from utils import build_keyboard_menu


# select_food_buttons_list = [
#     KeyboardButton('SelectFoodButtons.breakfast'),
#     KeyboardButton('SelectFoodButtons.breakfast'),
#     KeyboardButton('SelectFoodButtons.breakfast'),
#     KeyboardButton('SelectFoodButtons.breakfast'),
#     KeyboardButton('SelectFoodButtons.breakfast'),
# ]

# print(build_keyboard_menu(select_food_buttons_list, n_cols=2))