from telegram.ext import ConversationHandler
from handlers.workout_handlers.save_user_workout_handlers import save_user_workout_handler
from utils.navigation import (
    TYPE_TRAIN_KEY,
    CHOICE_TRAIN_KEY,
    GENERATE_TRAIN_KEY,
    GEN_EX_KEY,
    END_GENERATION_TRAIN_KEY,
    BACK_KEY,
    GO_2_PUSH_UP_TEST_KEY,
    PUSH_UP_TEST_KEY,
    RUNNING_3KM_TEST_KEY,
    SQUAT_TEST_KEY,
    PRESS_TEST_KEY,
    PULL_UP_TEST_KEY,
    MAIN_MENU_KEY
)
from handlers.workout_handlers.generate_workout_handlers import (
    select_feeling_handler,
    select_train_handler,
    generate_train_handler,
    generate_exercise_handler,
    add_review_handler,
    back_2_generate_train_menu_handler
)
from handlers.workout_handlers.test_workout_handlers import (
    begin_test_handler,
    go_2_test_train_handler,
    set_push_up_handler,
    back_2_train_menu_handler,
    back_2_main_menu_handler,
    set_running_3km_handler,
    set_squat_handler,
    set_press_handler,
    set_pull_up_handler,
    select_action_handler
)
from handlers.general_handlers import (
    encorrect_msg_choice_feeling_handler,
    encorrect_msg_choice_type_train_handler,
    encorrect_msg_handler,
    encorrect_msg_choice_train_handler
)


# Пройти тестовую тренировку
conv_test_train = ConversationHandler(
    entry_points=[begin_test_handler],
    states={
        GO_2_PUSH_UP_TEST_KEY: [
            go_2_test_train_handler,
            back_2_train_menu_handler
        ],
        PUSH_UP_TEST_KEY: [set_push_up_handler],
        RUNNING_3KM_TEST_KEY: [set_running_3km_handler],
        SQUAT_TEST_KEY: [set_squat_handler],
        PRESS_TEST_KEY: [set_press_handler],
        PULL_UP_TEST_KEY: [set_pull_up_handler]
        # COMPLETE_TEST_KEY: [workouts.complete_test_workout_handler]
    },
    fallbacks=[],
    map_to_parent={
        BACK_KEY: BACK_KEY,
        CHOICE_TRAIN_KEY: CHOICE_TRAIN_KEY
    },
    name="test_train_conversation",
    persistent = True,
)


# Сгенирировать тренировку
conv_generate_train = ConversationHandler(
    # entry_points=[select_train_handler], # ! Добавить в workout.select_train_handler проверку для выхода в случае не прохождения тестовой тренировки
    entry_points=[select_feeling_handler], # Проверка на прохождение тестовой тренировки и выбор тренировки
    states={
        TYPE_TRAIN_KEY: [
            select_train_handler, encorrect_msg_choice_feeling_handler
        ],
        GENERATE_TRAIN_KEY:[
            generate_train_handler, encorrect_msg_choice_type_train_handler,
        ],
        GEN_EX_KEY:[generate_exercise_handler, encorrect_msg_handler],
        END_GENERATION_TRAIN_KEY:[add_review_handler],
    },
    fallbacks=[back_2_generate_train_menu_handler],
    map_to_parent={
        BACK_KEY: CHOICE_TRAIN_KEY,
    },
    name="generate_train_conversation",
    persistent = True,
)


# Выбор типа тренировки
conv_workout = ConversationHandler(
    entry_points=[select_action_handler],
    states={
        CHOICE_TRAIN_KEY: [
            conv_test_train,
            conv_generate_train,
            back_2_main_menu_handler,
            save_user_workout_handler,
            encorrect_msg_choice_train_handler
        ],
    },
    fallbacks=[],
    map_to_parent={
        BACK_KEY: MAIN_MENU_KEY,
        MAIN_MENU_KEY: MAIN_MENU_KEY
    },
    name="workout_conversation",
    persistent = True,
)