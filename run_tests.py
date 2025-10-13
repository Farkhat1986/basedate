import subprocess
import sys
import webbrowser

def run_tests():
    # Запускает pytest и формирует allure-results
    print("Запуск тестов")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--maxfail=1", "--disable-warnings", "--alluredir=allure-results"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Вывод логов
    print(result.stdout.decode())
    print(result.stderr.decode())

    # Проверяем код возврата
    if result.returncode == 0:
        print("Тесты прошли успешно")
        generate_allure_report()
    else:
        print("Тесты не прошли")
        sys.exit(result.returncode)

def generate_allure_report():
    # Генерирует Allure отчёт и запускает сервер на localhost port можно проставить самостоятельно
    print("Генерация отчёта Allure")
    subprocess.run(["allure", "generate", "allure-results", "-o", "allure-report", "--clean"], check=True)

    # Запускаем Allure сервер
    port = 8080
    print(f"Запуск Allure отчёта на http://localhost:{port}")

    # Открываем страницу в браузере
    webbrowser.open(f"http://localhost:{port}")

    # Запускаем сервер
    try:
        subprocess.run(["allure", "serve", "allure-results", "-p", str(port)], check=True)
    except KeyboardInterrupt:
        print("\n Сервер остановлен пользователем.")

if __name__ == "__main__":
    run_tests()
