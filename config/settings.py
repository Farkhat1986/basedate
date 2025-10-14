"""
Конфигурация для интеграционных тестов WordPress REST API.

Загружает настройки из .env, формирует базовые параметры подключения
и определяет ожидаемые HTTP-статусы с использованием http.HTTPStatus
для избежания "магических" чисел в тестах.
"""

from http import HTTPStatus
import os
import base64
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
API_PREFIX = "/wp-json/wp/v2"

AUTH_USER = os.getenv("WP_USER")
AUTH_PASS = os.getenv("WP_PASS")

AUTH = (AUTH_USER, AUTH_PASS)
AUTH_VALUE = base64.b64encode(f"{AUTH_USER}:{AUTH_PASS}".encode()).decode()

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {AUTH_VALUE}"
}

TEST_CONFIGURATION = {
    "TIME_OUT": 10,
    "STATUS_CODE": HTTPStatus.OK,
    "STATUS_CODE_FIRST": HTTPStatus.CREATED,
    "STATUS_CODE_NOT_FOUND": HTTPStatus.NOT_FOUND,
    "STATUS_CODE_UNAUTHORIZED": HTTPStatus.UNAUTHORIZED,
    "STATUS_CODE_ACCEPTED": HTTPStatus.ACCEPTED,
    "STATUS_CODE_NO_CONTENT": HTTPStatus.NO_CONTENT
}
