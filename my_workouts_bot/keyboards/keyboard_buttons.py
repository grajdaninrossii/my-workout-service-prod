from strenum import StrEnum # для универсальности версий

'''
В дальнейшем кнопки перейдут в директурию keyboards и разобются по файлам!
'''

BACK_BUTTON_TEXT = 'Назад ⬅'

class BotInfoButtons(StrEnum):
    more_bot_info: str = 'Подробнее о тебе 👀'
    bot_skills_info: str = 'Твои скилы 🤔'
    beginning_quiz: str = 'Готов/а начать! 💪'


class GenderChoiceButtons(StrEnum):
    male: str = 'Мужской 👨‍🦱',
    female: str = 'Женский 👩‍🦰'


# Goal
class GoalChoiceButtons(StrEnum):
    mass: str = 'Масса 💪'
    maintenance: str = 'Поддержка 🔗'
    flexibility: str = 'Гибкость 🪢'
    endurance: str = 'Выносливость 🥷🏻'
    # endurance: str = 'Похудение 🥷🏻'


# Политика конфиденциальности
class PolicyAgreeButtonsButtons(StrEnum):
    document: str = 'Подробнее 🕵🏻'
    agree: str = 'Согласен 🤝'


# Основное меню
class MainMenuButtons(StrEnum):
    sport: str = 'Тренировки 🏓'
    food: str = 'Рацион 🥕'
    settings: str = 'Параметры ⚙️'
    progress: str = 'Прогресс 📊'


# Тренировки
class ChoiceTrainButtons(StrEnum):
    create: str = 'Создать 🦾'
    train: str = 'Сгенерировать 🔨'
    test_train: str = 'Тест 🧑‍💻'
    user_train: str = 'Моя тренировка 😎'
    back: str = BACK_BUTTON_TEXT


class Go2TestTrainButtons(StrEnum):
    yes: str = 'Да 🦾'
    no: str = BACK_BUTTON_TEXT


# Выбор типа тренировки
class TypeTrainButtons(StrEnum):
    fast: str = 'Быстрая 🏃'
    standart: str = 'Стандартная ⚡️'
    stretching: str = 'Растяжка 🤸'
    back: str = BACK_BUTTON_TEXT


# Выбор самочуствия
class SelectFeelingButtons(StrEnum):
    excellent : str = 'Отличное 💪'
    okey: str =  'Нормальное 👌'
    bad: str = 'Плохое ☹️'
    back: str = BACK_BUTTON_TEXT


# Выбор рациона
class SelectFoodButtons(StrEnum):
    breakfast: str = '🥪'
    bite: str = '🥛'
    lunch: str = '🍝'
    snack: str = '🍶'
    dinner: str = '🫕'
    before_sleep: str = '🍵'
    day: str = 'На день 🍴'
    back: str = BACK_BUTTON_TEXT


# Действия в тренировке
class ActionInTrainButtons(StrEnum):
    next_exercise: str = 'Следующее ➡'
    without_warmup: str = 'Без разминки ⁉️'
    back: str = BACK_BUTTON_TEXT


# Отзывы о тренировке
class TrainReviewButtons(StrEnum):
    hard: str = 'Тяжело 😰'
    easy: str = 'Легко 😎'
    optim: str = 'Оптимально 👌'


# Настройки
class SettingsButtons(StrEnum):
    profile: str = 'Обо мне 🙂'
    support: str = 'Помощь 🆘'
    back: str = BACK_BUTTON_TEXT


# Изменение пользовательских данных
class UserSettingsButtons(StrEnum):
    gender: str = '👫'
    age: str = '📆'
    weight: str = '⚖️'
    height: str = '📏'
    goal: str = '🎯'
    about_me: str = 'Мои данные 📋'
    back: str = BACK_BUTTON_TEXT


# Прогресс
class ProgressButtons(StrEnum):
    graphic: str = 'График 📊'
    back: str = BACK_BUTTON_TEXT
