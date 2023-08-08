from telegram.ext import ApplicationBuilder, PicklePersistence
from handlers import user_handlers, workout_handlers, food_handlers, general_handlers

from utils.navigation import *
from config.settings import BOT_TOKEN

from telegram.ext import ConversationHandler
from telegram import Update

from models import *
import asyncio
from utils import loop, public_url

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Response, Request
import uvicorn
from config.logger import logging

from fast_api_core.routers import user_workouts_router, bot_router


async def main() -> None:


    '''
    Мы создаем объект приложения (он связывает все вместе и следит за обновлениями с помощью Updater), закидываем туда токен и
    вызываем метод build, чтобы запустить нашего красавчика бота.
    В строке кода ниже автоматически настраиваются:
    - Updater доступный как application.updater (прием данных от ТГ боту)
    - Bot доступный как application.bot/application.updater.bot (более высокий уровень доступа к методам Bot API)
    - BaseRequest объект инициализирутся и готов к использованию под application.bot (отвечает за обработку фактических сетевых данных, т.е. отправку запросов в API бота)
    - различные другие компоненты, значения в которых также устанавливаются по-умолчанию.
    '''

    persistence = PicklePersistence(filepath="myworkoutbot")
    application = ApplicationBuilder().token(BOT_TOKEN).updater(None).persistence(persistence).build()

    # Точка входа в разговор
    conv_handler = ConversationHandler(
        # Вход в разговор
        entry_points=[user_handlers.start_handler],
        states={
            BOT_INFO_KEY: [
                user_handlers.get_bot_skills_info_handler,
                user_handlers.get_bot_info_handler,
                user_handlers.go_2_quiz_handler
            ],
            BEGINNING_QUIZ_KEY: [user_handlers.set_gender_quiz_handler],
            SECOND_QUESTION_KEY: [user_handlers.set_age_quiz_handler], # users.get_user_age_quiz_handler,
            THIRD_QUESTION_KEY: [user_handlers.set_height_quiz_handler],
            FOURTH_QUESTION_KEY: [user_handlers.set_weight_quiz_handler],
            FIFTH_QUESTION_KEY: [user_handlers.set_goal_quiz_handler],
            POLICY_KEY: [user_handlers.set_agree_policy_quiz_handler],
            MAIN_MENU_KEY:[
                workout_handlers.conv_workout,
                food_handlers.conv_food,
                user_handlers.conv_setting,
                user_handlers.conv_progress,
                # user_handlers.clear_handler,
                 
                # user_handlers.start_handler, # потом убрать!!!!!!!!!!!!
                general_handlers.encorrect_msg_main_handler # Должен проверяться последним
                ],
        },
        fallbacks=[],
        name="general_conversation",
        persistent = True,
    )

    # Прикрепляем наш обработчик к приложению
    application.add_handler(conv_handler)
    # application.add_handler(TypeHandler(type=WebhookUpdate, callback=webhook_update))

    # Передать настройки вебхука в телеграмм
    await application.bot.set_webhook(url=f"{public_url}/telegram")

    app = FastAPI()
    app.mount("/public", StaticFiles(directory="static/public"), name="public")
    app.mount("/css", StaticFiles(directory="fast_api_core/templates/css"), name="css")

    # Поднимаем веб-сервер
    @app.post("/telegram")
    async def telegram(update: Request) -> Response:
        """Обрабатываем входящие обновления Telegram, помещая их в `update_queue`"""
        await application.update_queue.put(
            Update.de_json(data=await update.json(), bot=application.bot)
        )
        return Response()

    app.include_router(bot_router)
    app.include_router(user_workouts_router)

    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=app,
            port=8000,
            use_colors=True,
            host="127.0.0.1",
            loop=loop,
            reload=True # Потом убрать
        )
    )

    # application.run_polling() # запуск ddos сервера телеграмма для проверки обновлений
    # # Запуск приложения и веб-сервера вместе
    async with application:
        await application.initialize()
        await application.start()

        await webserver.serve()

        await application.stop()
        await application.shutdown()


if __name__ == "__main__":
    asyncio.run(main())