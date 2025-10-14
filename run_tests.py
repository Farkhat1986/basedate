"""
Скрипт для запуска автоматизированных тестов и генерации отчёта Allure

Выполняет:
- Запуск тестов через pytest с сохранением результатов в allure-results,
- Генерацию HTML-отчёта Allure,
- Автоматическое открытие отчёта в браузере на localhost

Использует логирование для отслеживания хода выполнения и ошибок
"""

import subprocess
import sys
import webbrowser
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)
logger = logging.getLogger(__name__)


def run_tests():
    """
    Запускает тесты с помощью pytest и сохраняет результаты в формате Allure

    При успешном прохождении тестов вызывает генерацию отчёта
    При падении тестов — завершает выполнение с кодом ошибки
    """
    logger.info("Запуск тестов")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--maxfail=1", "--disable-warnings", "--alluredir=allure-results"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Вывод логов
    logger.info(result.stdout.decode())
    logger.error(result.stderr.decode())

    # Проверяем код возврата
    if result.returncode == 0:
        logger.info("Тесты прошли успешно")
        generate_allure_report()
    else:
        logger.error("Тесты не прошли")
        sys.exit(result.returncode)


def generate_allure_report():
    """
    Генерирует HTML-отчёт Allure и запускает встроенный сервер для просмотра

    Открывает отчёт автоматически в браузере по адресу http://localhost:8080
    Сервер можно остановить нажатием Ctrl+C
    """
    # Генерация Allure отчёта и запуск сервера на localhost
    logger.info("Генерация отчёта Allure")
    subprocess.run(["allure", "generate", "allure-results", "-o", "allure-report", "--clean"], check=True)

    # Запускаем Allure сервер
    port = 8080
    logger.info(f"Запуск Allure отчёта на http://localhost:{port}")

    # Открываем страницу в браузере
    webbrowser.open(f"http://localhost:{port}")

    # Запускаем сервер
    try:
        subprocess.run(["allure", "serve", "allure-results", "-p", str(port)], check=True)
    except KeyboardInterrupt:
        logger.info("Сервер остановлен пользователем")


if __name__ == "__main__":
    run_tests()