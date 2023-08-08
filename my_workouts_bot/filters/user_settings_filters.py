from telegram.ext import filters
from keyboards.keyboard_buttons import (
    GenderChoiceButtons,
    GoalChoiceButtons,
    PolicyAgreeButtonsButtons,
    MainMenuButtons,
    SettingsButtons,
    UserSettingsButtons,
    ProgressButtons
)

# quiz_filter
set_gender_filter = filters.Regex(f'^{GenderChoiceButtons.male}') | filters.Regex(f'^{GenderChoiceButtons.female}')

fset_goal_filter = filters.Regex(f'^{GoalChoiceButtons.mass}') | \
    filters.Regex(f'^{GoalChoiceButtons.flexibility}') | \
    filters.Regex(f'^{GoalChoiceButtons.endurance}') | \
    filters.Regex(f'^{GoalChoiceButtons.maintenance}')

policy_agree_filter = filters.Regex(f'^{PolicyAgreeButtonsButtons.agree}')

# Настройки
settings_filter = filters.Regex(f'^{MainMenuButtons.settings}')
support_filter = filters.Regex(f'^{SettingsButtons.support}')
user_settings_filter = filters.Regex(f'^{SettingsButtons.profile}')
choice_settings_filter = filters.Regex(f'^{UserSettingsButtons.gender}') | \
    filters.Regex(f'^{UserSettingsButtons.age}') | \
    filters.Regex(f'^{UserSettingsButtons.height}') | \
    filters.Regex(f'^{UserSettingsButtons.weight}') | \
    filters.Dice.Darts(list(range(1, 7)))

get_user_data_filter = filters.Regex(f'^{UserSettingsButtons.about_me}')

get_progress_filter = filters.Regex(f'^{MainMenuButtons.progress}')
get_progress_graphic_filter = filters.Regex(f'^{ProgressButtons.graphic}')