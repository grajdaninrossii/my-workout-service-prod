from itertools import count
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas as pd
from config.settings import POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_SERVER, POSTGRES_DB
import os


def fill_type_workout(cursor):
    types = ["обычная", "короткая", "йога", "растяжка"]
    query = """INSERT INTO type_workouts (TYPE_NAME) VALUES (%s)"""
    for r in types:
        cursor.execute(query, tuple([r]))


def fill_type_goal(cursor):
    types = ["набрать мышечную массу", "поддержать форму", "развить гибкости", "развить выносливости"]
    query = """INSERT INTO goals (GOAL_NAME) VALUES (%s)"""
    for r in types:
        cursor.execute(query, tuple([r]))


def fill_genders(cursor):
    types = ["мужской", "женский"]
    query = """INSERT INTO genders (GENDER_NAME) VALUES (%s)"""
    for r in types:
        cursor.execute(query, tuple([r]))


def fill_type_exercise(cursor):
    types = ["силовые", "выносливость", "статика", "растяжка", "разминка"]
    query = """INSERT INTO types_workout_exercise (TYPE_NAME) VALUES (%s)"""
    for r in types:
        cursor.execute(query, tuple([r]))


def fill_difficulty_level(cursor):
    levels = ["начальный", "опытный", "профессиональный", "адаптивный"]
    query = """INSERT INTO complexity_levels (COMPL_NAME) VALUES (%s)"""
    for r in levels:
        cursor.execute(query, tuple([r]))


def fill_inventories(cursor):
    inventories = ["отсутствует", "турник", "брусья"]
    query = """INSERT INTO inventories (INV_NAME) VALUES (%s)"""
    for r in inventories:
        cursor.execute(query, tuple([r]))


def fill_muscules(cursor):
    # 0 - руки, 1 - ноги, 2 - спина, 3 - пресс, 4 - шея
    muscules = ["руки", "ноги", "спина", "пресс", "шея"]
    query = """INSERT INTO muscules (MUSCULE_NAME) VALUES (%s)"""
    for r in muscules:
        cursor.execute(query, tuple([r]))


## !!!! ДОПИСАТЬ
def fill_exercise_muscules(ex_musl, cursor):
    query = """INSERT INTO muscule_exercise_groups (EXERCISE_ID, MUSCULES_ID) VALUES (%s, %s)"""
    for _, r in ex_musl.iterrows():
        # print()
        ex = r.tolist()
        for x in eval(ex[1]):
            cursor.execute(query, tuple([ex[0], x]))


# ,ex_name,id_type_exercise,id_difficulty_level,id_inventory,id_muscule_group,description,technique,url_image_exercise
def fill_exercises(exercise_db_without_muscules, cursor):
     # Добавляем наши упражнения
    insert_stuff_query = """ INSERT INTO exercises (EX_NAME, TYPE_EXERCISE_ID,
                               COMPLEXITY_LEVEL_ID, INVENTORIES_ID, DESCRIPTION, TECHNICES, IMAGE_EXERCISE_URL
                             )
                             VALUES (%s,%s,%s,%s,%s,%s,%s)"""
                             
    # update_stuff_query = """ UPDATE exercises SET EX_NAME = %s, TYPE_EXERCISE_ID = %s,
    #                            COMPLEXITY_LEVEL_ID = %s, INVENTORIES_ID = %s
    #                            , DESCRIPTION = %s, TECHNICES = %s, IMAGE_EXERCISE_URL = %s
    #                            WHERE id = %s"""
    # count = 0
    # for _, row in exercise_db_without_muscules.iterrows():
    #     stf = row.tolist()
    #     count += 1
    #     stf.append(count)
    #     stf = tuple(stf)
    #     cursor.execute(update_stuff_query, stf)

    # ,productDisplayName,gender,masterCategory,articleType,baseColor,season,usage,imageUrl,urlSource
    for _, row in exercise_db_without_muscules.iterrows():
        stf = row.tolist()
        # print(stf)
        stf = tuple(stf)
        cursor.execute(insert_stuff_query, stf)


# Делаем здесь функцию для заполнения блюд
def fill_dishes(dish_db, cursor):
    # id,title,kcal,proteins,fats,carbohydrates,isPiece,category,default_weight,max_weight
    # Добавляем наши упражнения
    insert_stuff_query = """ INSERT INTO dishes (TITLE, KILOCALORIES,
                               PROTEINS, FATS, CARBOHYDRATES, IS_PIECE, CATEGORY, DEFAULT_WEIGHT, MAX_WEIGHT
                             )
                             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    for _, row in dish_db.iterrows():
        stf = row.tolist()
        stf[-4] = bool(stf[-4])
        # print(stf)
        stf = tuple(stf)
        cursor.execute(insert_stuff_query, stf)


def fill_feelings(cursor):
    # 0 - руки, 1 - ноги, 2 - спина, 3 - пресс, 4 - шея
    muscules = ["Отличное", "Нормальное", "Плохое"]
    query = """INSERT INTO feelings (FEELING_NAME) VALUES (%s)"""
    for r in muscules:
        cursor.execute(query, tuple([r]))
        

def fill_reviews(cursor):
    # 0 - руки, 1 - ноги, 2 - спина, 3 - пресс, 4 - шея
    muscules = ["Тяжело", "Легко", "Оптимально"]
    query = """INSERT INTO reviews (REVIEW_NAME) VALUES (%s)"""
    for r in muscules:
        cursor.execute(query, tuple([r]))



def load_data():
    # --------------------------Начало ---------------------------
    print(os.listdir())
    exercise_db = pd.read_csv("./data_csv/data__exercise.csv", delimiter=",")
    # print(exercise_db)
    exercise_db_without_muscules = exercise_db.loc[ : , exercise_db.columns != 'id_muscule_group']
    del exercise_db_without_muscules['id']
    # print(exercise_db_without_muscules.head())
    # print(exercise_db_without_muscules['id_difficulty_level'].unique())
    ex_muscule = exercise_db.loc[ : , ['id', 'id_muscule_group']]
    # print(ex_muscule)
    # print(exercise_db.head())

    dish_df = pd.read_csv("./data_csv/dish.csv", delimiter=",", index_col='id')
    # print(dish_df)

    connection = None
    # Добавление нашей красоты в бд
    try:
        # Поключение к нашей MyWorkouts бд
        connection = psycopg2.connect(user=POSTGRES_USER,
                                    password = POSTGRES_PASSWORD,
                                    host=POSTGRES_SERVER[:5],
                                    port=POSTGRES_SERVER[6:],
                                    database=POSTGRES_DB)
        # print('kek')
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        # Чекним инфу о бд
        print("Инфа о сервере PostgreSQL")
        # record = cursor.fetchone()
        # print("Вы подключены к - ", record, "\n")

        fill_type_workout(cursor)
        print("Типы тренировок заполнены")

        fill_type_goal(cursor)
        print("Цели заполнены")

        fill_genders(cursor)
        print("Полы заполнены))")

        fill_type_exercise(cursor)
        print("Типы упражнений заполнены")

        fill_difficulty_level(cursor)
        print("Уровни сложности заполнены")

        fill_inventories(cursor)
        print("Инвентарь заполнен")

        fill_muscules(cursor)
        print("Группы мышц заполнены")

        fill_exercises(exercise_db_without_muscules, cursor)
        print("Упражнения заполнены")

        fill_exercise_muscules(ex_muscule, cursor)
        print('Мышечные группы заполнены')

        fill_dishes(dish_df, cursor)
        print('Заполнение блюд')

        fill_feelings(cursor)
        print('Состояния заполнены')

        fill_reviews(cursor)
        print('Отзывы заполнены')

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


if __name__=="__main__":
    load_data()