from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse


bot_router = APIRouter()
from config.settings import templates
from config.logger import logging


@bot_router.get("/policy", response_class=HTMLResponse)
async def add_user_workouts(request: Request):
    # logging.debug(f"Что в запросе? {await request.body()}")
    return templates.TemplateResponse(
        name="policy.html",
        context={"request": request}
    )

@bot_router.get("/")
async def root():
    return {"message": "Hello World"}