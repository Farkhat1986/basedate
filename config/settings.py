"""
Конфигурация для интеграционных тестов WordPress REST API

Загружает настройки из .env, формирует базовые параметры подключения
и определяет ожидаемые HTTP-статусы с использованием HTTPStatus
для избежания "магических" чисел в тестах
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

TEST_CONFIGURATION = {

}