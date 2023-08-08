from copy import deepcopy
import random
from models import async_session
from models import User, Exercise, ExamWorkout
from models.workout import ExerciseUserWorkout, UserWorkout

from repositories import user_repo, ex_repo

from utils import MaxValueTrainError, MaxRunningValueTrainError
from utils import loop

import re
from config.logger import logging

from keyboards.keyboard_buttons import ChoiceTrainButtons, TypeTrainButtons, SelectFeelingButtons
from tensorflow.keras.models import load_model

# neuronet_model = keras.models.load_model('./neuronet_models/model_6')
import os
print(os.listdir())
# neuronet_model = keras.models.load_model('./neuronet_models/model_6')
neuronet_model = load_model('./neuronet_models/model_6')

exam_train_ex_id_list = [1, 22, 14, 2, 4]

# Потом постараться вынести в бд
workout_type_ex_count = {
    'crossfit': {
        'count_power_ex': 4,
        'count_warmup': 10,
        'count_stretch': 5,
        'type_exercise_id': 1,
        'muscules': [1, 2, 3, 4] # [1, 2, 3, 4, 5]
    },
    'EMOM': {
        'count_power_ex': 2,
        'count_warmup': 10,
        'count_stretch': 5,
        'type_exercise_id': 1,
        'muscules': [1, 2, 3, 4]
    },
    'statics': {
        'count_power_ex': 6,
        'count_warmup': 10,
        'count_stretch': 9,
        'type_exercise_id': 3,
        'muscules': [1, 2, 3, 4]
    },
    'power_hands': {
        'count_power_ex': 4,
        'count_warmup': 10,
        'count_stretch': 7,
        'type_exercise_id': 1,
        'muscules': [1, 4]
    },
    'power_legs': {
        'count_power_ex': 4,
        'count_warmup': 10,
        'count_stretch': 7,
        'type_exercise_id': 1,
        'muscules': [2, 4]
    },
    'power_complexity': {
        'count_power_ex': 6,
        'count_warmup': 10,
        'count_stretch': 7,
        'type_exercise_id': 1,
        'muscules': [1, 2, 4]
    },
    'stretching': {
        'count_power_ex': 0,
        'count_warmup': 10,
        'count_stretch': 8,
        'type_exercise_id': 4,
        'muscules': [1, 2, 3, 4, 5]
    }
}


async def add_test_exercise(user_id: int, ex_id: int, value: str) -> str:
    bot_answer: str = ''
    async with async_session() as session:
        try:
            user: User = await user_repo.get_one_user(session, user_id)
            exercise: Exercise = await ex_repo.get_one_ex(session, ex_id)

            # 22 -id бег на 3 км
            if exercise.id == 22 or exercise.id == 23:
                # if len(value.split('.')) not in range(1, 3):
                if re.search("^\d\d[:.]\d\d$", value) is None:
                    raise MaxRunningValueTrainError
            elif int(value) not in range(201):
                raise MaxValueTrainError

            ex_work: ExamWorkout = await ex_repo.get_one_exam_workout(session, user_id, ex_id)
            if ex_work is None:
                ex_work = ExamWorkout(values=value)
                ex_work.exercise = exercise
                user.exercises.append(ex_work)
            else:
                ex_work.values = value
            await session.commit()
            bot_answer = f'Данные сохранены!'
        except (MaxRunningValueTrainError, MaxValueTrainError) as e:
            bot_answer = str(e)
        except ValueError:
            bot_answer = 'Ошибка ввода, нужно вводить цифры!'
    return bot_answer


# Проврека прохождения тестовой тренировки
async def has_exam_train(user_id: int) -> bool:
    is_completed = False
    async with async_session() as session:
        ex_work_user: list[ExamWorkout] = await ex_repo.get_exam_exs_user(session, user_id)
        if ex_work_user == []:
            return is_completed
        ex_id_list = [x.exercise_id for x in ex_work_user]
        if all([i in ex_id_list for i in exam_train_ex_id_list]):
            is_completed = True
        # logging.debug('Результат запроса" {ex_work_user}')
        # logging.debug('Результат if {is_completed}')
        return is_completed


# Генерация тренировки
async def generate_exercise(
    user: User,
    user_feeling: str,
    type_train: str,
    current_exercise_number: int,
    template_train: str = None,
    last_exercise_id: int = None
) -> tuple[Exercise, str, int]:
    async with async_session() as session:

        # Получаем id самочуствия
        feeling_id = 1
        match user_feeling:
            case SelectFeelingButtons.bad:
                feeling_id = 3
            case SelectFeelingButtons.okey:
                feeling_id = 2

        if type_train == ChoiceTrainButtons.user_train:
            last_user_workout: int = await ex_repo.get_last_user_workout(session, user.id)
            current_exercises = await ex_repo.get_user_exercises(session, last_user_workout.id)
            if current_exercise_number < len(current_exercises):
                current_exercise = current_exercises[current_exercise_number]
                return current_exercise.user_exercise, None, None, current_exercise
            return None, None, None, None
        if template_train is None:
            if type_train == TypeTrainButtons.stretching:
                template_train = 'stretching'
            else:
                # Выбор типа тренировки
                list_program_train: list = []
                match user.goal_id:
                    case 1:
                        list_program_train = ['power_hands', 'power_legs', 'power_complexity']
                    case 2:
                        list_program_train = ['crossfit', 'EMOM', 'statics']
                    case 3:
                        list_program_train = ['crossfit', 'power_complexity', 'stretching', 'stretching']
                    case 4:
                        list_program_train = ['crossfit', 'EMOM', 'statics', 'power_hands', 'power_legs', 'power_complexity']
                template_train = random.choice(list_program_train) # Рандомный выбор

        train: dict = deepcopy(workout_type_ex_count[template_train])
        match (template_train, type_train):
            case ('power_hands' | 'power_legs' | 'power_complexity' | 'static', TypeTrainButtons.fast):
                train['count_power_ex'] = int(train['count_power_ex'] * 0.75)
        # Если это разминка
        if current_exercise_number < train['count_warmup']:
            all_warmup_ex: list[Exercise] = await ex_repo.get_all_exercise_with_where(session, 5) # делаем запрос на получения разминочного упражения
            return all_warmup_ex[current_exercise_number], template_train, None, None
        # Если это основные упражнения
        elif (current_exercise_number - train['count_warmup']) < train['count_power_ex']:
            if last_exercise_id is None:
                # logging.debug(f"test {random.choice(train['muscules'])}, {random.choice(train['muscules'])}")
                current_exercise: list[Exercise] = await ex_repo.get_first_exercise_with_3_where(
                    session=session,
                    type_exercise_id=train['type_exercise_id'],
                    not_ex_id=-1,
                    muscule_id=random.choice(train['muscules'])
                )
            else:
                # last_exercise: Exercise = await ex_repo.get_one_ex(session, last_exercise_id)
                muscule_id = 1
                muscules_last_ex: list = [x.id for x in await ex_repo.get_ex_muscules(session, last_exercise_id)]
                # allow_muscules = 
                # logging.debug(f'Смотрим ошибку {muscules_last_ex[0].id}')
                muscule_last_ex_id = list([m for m in muscules_last_ex if m in train['muscules']])[0]
                # logging.debug(f'Смотрим ошибку 4 {len(muscules_last_ex)}')
                # !!!!!!!! Переписать ниже выбор упражнений под истроию тренировок
                match template_train:
                    case 'power_hands' | 'power_legs' | 'power_complexity'|'crossfit'|'EMOM'|'statics':
                        # muscule_last_ex_id = muscule_last_ex.id
                        logging.debug(f"Проблемы с id_ex {muscule_last_ex_id}, {list([m for m in muscules_last_ex if m in train['muscules']])}, {template_train}")
                        train['muscules'].remove(muscule_last_ex_id)
                        muscule_id = random.choice(train['muscules'])
                    case 'stretching':
                        raise ValueError
                logging.debug(f"Странно {muscule_id}, {train['type_exercise_id']}")
                exercises: list[Exercise] = await ex_repo.get_all_ex_muscules_with_conds(session, muscule_id, train['type_exercise_id'])
                current_exercise = exercises[0]
            if current_exercise.id < 22:
                ################### NEURONET
                count = await get_neuronet_data(session, user, current_exercise, feeling_id)
                return current_exercise, template_train, count, None
            return current_exercise, template_train, None, None
        # Если это расстяжка
        elif (current_exercise_number - (train['count_warmup'] + train['count_power_ex'])) < train['count_stretch']:
            all_stretching_ex: list[Exercise] = await ex_repo.get_first_exercise_with_2_where(session, 4, last_exercise_id)
            return all_stretching_ex, template_train, None, None
        else:
            return None, None, None, None


async def get_neuronet_data(session, user: User, ex: Exercise, feelling_id: int) -> int:
    test_ex_id_sorted: list[int] = await ex_repo.get_all_ex_id_in_exam_workout(session, user.id, exam_train_ex_id_list) # exam_ex_ids
    test_ex = []
    for ex_id, value in test_ex_id_sorted:
        if ex_id == 22 and ':' in value:
            value = '.'.join(value.split(':'))
        value = float(value)
        test_ex.append((ex_id, value))
    # id_exercise	push_ups	running_3km	squats	press	pull_ups	id_gender	age	feeling	target_count
    # [1, 22, 14, 2, 4]
    data: list[float] = [
        ex.id,
        test_ex[0][1],
        test_ex[4][1],
        test_ex[1][1],
        test_ex[3][1],
        test_ex[2][1],
        user.gender_id,
        user.age,
        feelling_id
        ]
    logging.debug(f'Характеристики {data}')
    predict_target = round(neuronet_model.predict(data)[0][0])
    ### Мега костыль, хз пока сломалось
    if ex.id == 3:
        predict_target = round(predict_target * 0.8)
    # elif ex.id == 13:
    #     predict_target = round(predict_target * 0.3)
    return predict_target


async def save_user_workout(
    data: list,
    user_id: int
    ) -> bool:
    async with async_session() as session:
        if data == []:
            return False
        # ПОМЕНЯТЬ ЗАПРОС ИЛИ ДОБАВИТЬ ДЛЯ ПОДСЧЕТА И ПРОВЕРКИ КОЛИЧЕСТВА ДОБАВЛЕННЫХ ТРЕНИРОВОК (ТАКЖЕ ДОБАВИТЬ ИНТЕРФЕЙС ДЛЯ УДАЛЕНИЯ ТРЕНИРОВКИ)
        last_id: int | None = await ex_repo.get_last_user_workout_id(session)
        user_workout_id = 1
        if last_id is not None:
            user_workout_id += last_id
        # logging.debug(f"смотрим data: {data}")
        user_workout: UserWorkout | None = await ex_repo.add_new_user_workout(session, user_id, user_workout_id)
        exercises: list[ExerciseUserWorkout] = [ExerciseUserWorkout(user_workout_id, ex_id, approach, "10", 60, n) for n, (ex_id, approach) in enumerate(data)]
        rezult = await ex_repo.add_new_exs_user_workout(session, exercises)
        await session.commit()
        return rezult


async def is_exist_user_workouts(
    user_id: int
) -> bool:
    async with async_session() as session:
        rezult = True
        last_id: int | None = await ex_repo.get_last_user_workout_id(session)
        if last_id is None:
            rezult = False
        return rezult