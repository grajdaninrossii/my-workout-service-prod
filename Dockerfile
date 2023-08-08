# Dockerfile
FROM python:3.11 as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

# устанавливаем рабочую директорию
WORKDIR /my_workouts_bot

FROM base as builder

# устанавливаем переменные окружения ждя версий библиотек и т.д.
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.4.2

# обновляем пакеты, устанавливаем локализацию
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"
# RUN python -m venv /venv

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./my_workouts_bot/pyproject.toml ./my_workouts_bot/poetry.lock* /my_workouts_bot/

# COPY pyproject.toml poetry.lock ./
# устанавливаем poetry (без virtualenvs.create false не видит нужные файлы).
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi
# RUN pip install python-telegram-bot

RUN poetry run pip install --no-cache-dir --upgrade tensorflow==2.12.0
RUN poetry run pip install pyngrok


COPY ./my_workouts_bot /my_workouts_bot
# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
# ARG INSTALL_JUPYTER=false
# RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"



ENV PYTHONPATH /my_workouts_bot/
# RUN alembic upgrade head
# CMD ["prestart.sh"]