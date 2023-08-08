from telegram.ext import filters
from keyboards.keyboard_buttons import BotInfoButtons

bot_info_filter = filters.Regex(f'^{BotInfoButtons.more_bot_info}$')
bot_skills_filter = filters.Regex(f'^{BotInfoButtons.bot_skills_info}$')
beginning_quiz_filter = filters.Regex(f'^{BotInfoButtons.beginning_quiz}$')