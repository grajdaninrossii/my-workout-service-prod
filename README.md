# Сервис MyWorkouts
 Проект создан на базе телеграм бота. В ближайшем времени планируется реализация сайта с дополнительной информацией о тренировках и питании.

## Технологии
В проекте используются:
1. Python 3.11 и его стандартные библиотеки
2. Numpy/Pandas для работы с данными
3. Tensorflow для обучения модели нейросети
4. Python-telegram-bot для упрощения реализации бота
5. SqlAlchemy для работы с бд на базе ORM
6. Postgres для хранения данных
7. Alembic для создание миграций баз данных
8. Менеджер пакетов Poetry
9. Docker, Docker compose

## Функционал
### Реализовано
На данный момент уже реализовано:
* добавление данных пользователя;
* прохождение тестовой тренировки;
* генерация тренировки с учётом тестовой тренировки и данных пользователя;
* генерации питания с учётом данных пользователя;
* интерфейс изменения данных пользователя;
* учет статистики тренировок;
* миграции базы данных;
* серверная часть для упрощения возможности упрощения пользовательского интерфейса;
* контеризация.

### В разработке

* улучшение генерации тренировок, добавление учёта уровня пользователя при подборе упражнения;
* улучшение системы подбора питания;
* и многое другое 😉

## Дополнительно
В репозитории приложены скрипты обучения модели нейронной сети и заполнения базы данных стандартными значениями.

Также много значений берется из csv файлов, которые создавались нами вручную для заполнения базы данных и для обучения нейросети.

## О нейросети
Так как полученные нами данные очень ограниченны в выборке было решено собирать данные проведенных тренировок и дообучать нейросеть на них.

Данный интерфейс появится в новых версиях сервиса.

## Ссылки
[MyWorkoutsBot](https://t.me/my_workouts_bot) (В момент разработки может быть неактивным)
