from typing import List
import random
import asyncio

from repositories import dish_repo, user_repo
from models import async_session, User
from config.logger import logging
from keyboards.keyboard_buttons import SelectFoodButtons
from utils import loop


async def get_dish_list() -> list:
    async with async_session() as session:
        dish_list_tuple = await dish_repo.get_all_dishes(session)
        dish_list = [list(x) for x in dish_list_tuple]
    return dish_list


# Функция получения рациона на день
async def get_day_ration(user_id: int)  -> str:
    async with async_session() as session:
        type_dish_goal_id_1 = [
            SelectFoodButtons.breakfast,
            SelectFoodButtons.bite,
            SelectFoodButtons.lunch,
            SelectFoodButtons.snack,
            SelectFoodButtons.dinner,
            SelectFoodButtons.before_sleep
        ]
        type_dish_other_goal = [
            SelectFoodButtons.breakfast,
            SelectFoodButtons.lunch,
            SelectFoodButtons.snack,
            SelectFoodButtons.dinner
        ]
        current_user: User = await user_repo.get_one_user(session, user_id)

    dish_types = type_dish_other_goal
    if (current_user.goal_id == 1):
        dish_types = type_dish_goal_id_1
    ration = 'Рацион на день:\n'
    for type_dish in dish_types:
        ration = ration + await get_one_ration(
            user_id=user_id,
            str_meal=type_dish,
        ) + '\n'
    return ration


# Метод получения рациона на завтрак
# str_meal: str = {"завтрак", "перекус", "обед", "полдник", "ужин", "перед сном"}
async def get_one_ration(user_id: int, str_meal: str)  -> str:
    async with async_session() as session:
        current_user: User = await user_repo.get_one_user(session, user_id)
        gender_id = current_user.gender_id
        goal_id = current_user.goal_id
        age = current_user.age
        weight = current_user.weight
        height = current_user.height
        count_train_by_week = 3

        needKPFC = await getKPFC(gender_id, goal_id, age, weight, height, count_train_by_week)

        match str_meal:
            case SelectFoodButtons.breakfast:
                type_meals = [[9,3], [4,9], [9]] # Разновидности завтраков по типу (1+2+3 категория блюд / 1+4 категория блюд и тд)
                PERCENT_KCAL = 0.1
                PERCENT_PROTEINS = 0.1
                PERCENT_FATS = 0.1
                PERCENT_CARBOHYDRATES = 0.1
                PERCENT_ERROR = 0.04
                title = 'Завтрак 🥪:'
            case SelectFoodButtons.bite:
                type_meals = [[11], [11], [11, 4], [2,4]]
                PERCENT_KCAL = 0.1
                PERCENT_PROTEINS = 0.15
                PERCENT_FATS = 0.15
                PERCENT_CARBOHYDRATES = 0.15
                PERCENT_ERROR = 0.05
                title = 'Перекус 🥛:'
            case SelectFoodButtons.lunch:
                type_meals = [[5, 2, 1, 3], [5,2,3], [5,2,1], [5,1], [5,3,6], [5,1,7], [10,3,2]]
                PERCENT_KCAL = 0.25
                PERCENT_PROTEINS = 0.25
                PERCENT_FATS = 0.25
                PERCENT_CARBOHYDRATES = 0.25
                PERCENT_ERROR = 0.05
                title = 'Обед 🍝:'
            case SelectFoodButtons.snack:
                type_meals = [[4], [2,3], [4,3]]
                PERCENT_KCAL = 0.15
                PERCENT_PROTEINS = 0.15
                PERCENT_FATS = 0.15
                PERCENT_CARBOHYDRATES = 0.15
                PERCENT_ERROR = 0.05
                title = 'Полдник 🍶:'
            case SelectFoodButtons.dinner:
                type_meals = [[8,1,3], [8,1,3], [0,1,3], [0,1,2,3], [10,2,3], [10,3], [10,2,3,6], [0,1,2,6]]
                PERCENT_KCAL = 0.25
                PERCENT_PROTEINS = 0.25
                PERCENT_FATS = 0.25
                PERCENT_CARBOHYDRATES = 0.25
                PERCENT_ERROR = 0.05
                title = 'Ужин 🫕:'
            case SelectFoodButtons.before_sleep:
                type_meals = [[11, 9], [4]]
                PERCENT_KCAL = 0.15
                PERCENT_PROTEINS = 0.1
                PERCENT_FATS = 0.1
                PERCENT_CARBOHYDRATES = 0.1
                PERCENT_ERROR = 0.04
                title = 'Перед сном 🍵:'


        typeMeal = random.choice(type_meals) # Рандомно выбранный вариант завтрака

        # Формируем и стабилизируем рацион
        listRation = await getPartDayRation(typeMeal=typeMeal, dishList = dish_list, needKCal=PERCENT_KCAL*needKPFC[0], needProtein=PERCENT_PROTEINS*needKPFC[1], 
                                            needFats=PERCENT_FATS*needKPFC[2], needCarbohydrates=PERCENT_CARBOHYDRATES*needKPFC[3], percentError=PERCENT_ERROR)

        # Формируем строку с завтраком
        ration = title
        for dish in listRation:
            if (dish[8] > 0):
                ration += f"\n • {dish[1]} - {dish[8]} {'шт' if dish[6]==1 else 'г'}"
    return ration


#Функция составления рациона на часть дня (завтрак/обед/ужин и тд)
async def getPartDayRation(typeMeal: List, dishList: List, needKCal: float, needProtein: float, needFats: float, needCarbohydrates: float, percentError: float) -> List:
    #Проходимся по каждому пункту завтрака 1), 2), 3) и тд, формируя рацион listRation на завтрак
    listRation = []
    for category in typeMeal:
        dishFromCategory = random.choice(list(filter(lambda dish: dish[7]==category, dishList)))
        listRation.append(dishFromCategory)

    #Стабилизируем разграммовку
    await stabilizeByParametrs(listRation=listRation, needKCal=needKCal, needProtein=needProtein, needFats=needFats, needCarbohydrates=needCarbohydrates, percentError=percentError)

    return listRation


# #Функция получения рациона на неделю
# async def getWeekRation(gender_id: int, goal_id: int, age: int, weight: float, height: float, countTrainByWeek: int)  -> str:
#     resultStr: str = ""
#     for i in range(7):
#         resultStr += f"День {i+1}\n{getDayRation(gender_id, goal_id, age, weight, height, countTrainByWeek)}\n--------\n"
#     return resultStr


# Метод подсчета суммы для одного из параметров (ккал или БЖУ)
async def getSumByParametr(listRation: List, indexParametr: int) -> float:
    sumParametr = 0
    for dish in listRation:
        sumParametr += dish[indexParametr]*dish[8]/(100.0, 1.0)[dish[6]==1]

    return sumParametr


# Метод стабилизации рациона по параметру (подгоняет массу блюд в зависимости от параметра )
async def stabilizeByParametr(listRation: List, indexParametr: int, needParametr: float, percentError: float):

            MAX_COUNT_WHILE = 3                         # Число максимальных добавок/убавок массы за одну стабилизацию
            COUNT_RANDOM_DISH_FOR_INCREMENT_CHOICE = 5  # Среди скольких самых каллорийных блюд будет сделан выбор для увеличения параметра (ккал)
            VALUE_ADD_DELETE_WEIGHT_1 = 1               # Минимальный размер порции для добавки/убавки (поштучно)
            VALUE_ADD_DELETE_WEIGHT_2 = 100             # Минимальный размер порции для добавки/убавки (пограммово)
            # VALUE_ADD_DELETE_WEIGHT_2 = 50            # Минимальный размер порции для добавки/убавки (пограммово)


            sumParametr = await getSumByParametr(listRation, indexParametr)
            arrayIndexMaxParametrProduct = await getIndexesRowByMaxColumn(listRation, indexParametr)


            #Проверяем на ккал
            countWhile=0
            while (sumParametr < (1-percentError)*needParametr):
                #На всякий случай проверка на бесконечный цикл
                if (countWhile >= MAX_COUNT_WHILE):
                    break

                #indexMaxProduct = arrayIndexMaxParametrProduct[random.randint(0,COUNT_RANDOM_DISH_FOR_INCREMENT_CHOICE+1)] #Индекс самого каллорийного продукта
                indexMaxProduct = arrayIndexMaxParametrProduct[random.randint(0,COUNT_RANDOM_DISH_FOR_INCREMENT_CHOICE+1 if len(listRation)>=COUNT_RANDOM_DISH_FOR_INCREMENT_CHOICE+1 else len(listRation)-1)] #Индекс самого каллорийного продукта
                if (listRation[indexMaxProduct][6] == 1):
                    if (listRation[indexMaxProduct][8] < listRation[indexMaxProduct][9]):
                        listRation[indexMaxProduct][8] += VALUE_ADD_DELETE_WEIGHT_1
                else:
                    if (listRation[indexMaxProduct][8] < listRation[indexMaxProduct][9]):
                        listRation[indexMaxProduct][8] += VALUE_ADD_DELETE_WEIGHT_2
                countWhile+=1

            countWhile=0
            while (sumParametr > (1+percentError)*needParametr):
                #На всякий случай проверка на бесконечный цикл
                if (countWhile >= MAX_COUNT_WHILE):
                    break

                #Выбираем оставшиеся самые мощные продукты (на случай если минусовали массу и там вышел ноль)
                indexMaxNotNullProduct = 0
                for currentIndex in arrayIndexMaxParametrProduct:
                    if (listRation[currentIndex][8] > VALUE_ADD_DELETE_WEIGHT_2):
                        indexMaxNotNullProduct = currentIndex
                        break
                #print("Уменьшаем ккал: ", listRation[indexMaxNotNullProduct])

                #addWeight = round((sumKCal - needKPFC[0]) / listRation[indexMaxNotNullProduct][2]) #Сколько порций 100г/шт еще нужно добавить
                if (listRation[indexMaxNotNullProduct][6] == 1):
                    listRation[indexMaxNotNullProduct][8] -= VALUE_ADD_DELETE_WEIGHT_1
                    if (listRation[indexMaxNotNullProduct][8] < VALUE_ADD_DELETE_WEIGHT_1):
                        listRation[indexMaxNotNullProduct][8] = VALUE_ADD_DELETE_WEIGHT_1
                else:
                    listRation[indexMaxNotNullProduct][8] -= VALUE_ADD_DELETE_WEIGHT_2
                    if (listRation[indexMaxNotNullProduct][8] < VALUE_ADD_DELETE_WEIGHT_2):
                        listRation[indexMaxNotNullProduct][8] = VALUE_ADD_DELETE_WEIGHT_2
                    #Небольшая фича только для мяса - (категория 1)
                    if (listRation[indexMaxNotNullProduct][8] < 100 and listRation[indexMaxNotNullProduct][7]==1):
                        listRation[indexMaxNotNullProduct][8] = 100
                countWhile+=1


#Метод стабилизации по каллориям и белкам (жирам и углеводам - в дальнейшем) N раз
async def stabilizeByParametrs(listRation: List, needKCal: float, needProtein: float, needFats: float, needCarbohydrates: float, percentError: float):
    N_STAB = 12 #Число повторных стабилизаций

    #Корректируем массу рациона
    for i in range(N_STAB):

        #Стабилизация по ккал
        await stabilizeByParametr(listRation, 2, needKCal, percentError)

        #Стабилизация по белкам
        await stabilizeByParametr(listRation, 3, needProtein, percentError)


#Метод получения списка индексов строк отсортированных по столбцу indexColumn в порядке убывания
async def getIndexesRowByMaxColumn(arrayRation, indexColumn: int) -> List[int]:
    copyArrayRation = arrayRation.copy()
    copyArrayRation.sort(key=lambda x: x[indexColumn], reverse=True)
    arrayIndexes = []
    for dish in copyArrayRation:
        arrayIndexes.append(arrayRation.index(dish))

    return arrayIndexes


#Функция подсчета каллорий и соотношения белков, жиров и углеводов
async def getKPFC(gender_id: int, goal_id: int, age: int, weight: float, height: float, countTrainByWeek: int) -> List[float]:
    kcal: float = 0 #Необходимое число каллорий

    #Каллории для поддержания формы
    KFA: float = await getKFA(countTrainByWeek)
    if (gender_id == 1):
        #Мужчина
        kcal = KFA * (66.5 + (13.75 * weight) + (5.003 * height) - (6.775 * age))
    elif (gender_id == 2):
        #Не мужчина
        kcal = KFA * (655.1 + (9.563 * weight) + (1.85 * height) - (4.676 * age))

    #Перерасчет каллорий в зависимости от цели тренировок
    if (goal_id == 1):
        #Набор массы
        kcal *= 1.2
        proteins = weight*1.5
        return [kcal, proteins, proteins/0.375*0.2, proteins/0.375*0.425]
    elif (goal_id == 2 or goal_id == 3):
        #Поддержание массы и гибкость
        proteins = weight*0.8
        return [kcal, proteins, proteins, proteins/0.3*0.4]
    elif (goal_id == 4):
        #Сильнее и выносливее
        kcal *= 1.05
        proteins = 0.95*weight
        return [kcal, proteins, proteins, proteins/0.225*0.55]


#Функция, возвращающая коэффициент каллорий для поддержания формы в зависимости от числа тренировок в неделю
async def getKFA(countTrainByWeek: int) -> float:
    result: float = 1.2

    if countTrainByWeek == 0:
        result = 1.2
    elif countTrainByWeek <= 2:
        result = 1.375
    elif countTrainByWeek <= 4:
        result = 1.55
    elif countTrainByWeek <= 7:
        result = 1.7
    else:
        result = 1.9

    return result


dish_list = loop.run_until_complete(get_dish_list())