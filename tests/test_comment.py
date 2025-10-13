import allure
from config.settings import TEST_CONFIGURATION
from db.db_connection import get_comment_from_db
from data.data_comments import updated_comment_data, comment_data

@allure.feature("Комментарии")
@allure.story("Создание комментария")
def test_create_comment(comments_api, created_post):
    with allure.step(f"Создание комментария для поста {created_post['id']}"):
        response = comments_api.create(comment_data)
        assert response.status_code == TEST_CONFIGURATION["STATUS_CODE_FIRST"]
        comment = response.json()

    with allure.step("Проверка комментария в БД"):
        db_comment = get_comment_from_db(comment["id"])
        assert db_comment is not None
        assert db_comment.comment_content == "Тестовый комментарий"

@allure.feature("Комментарии")
@allure.story("Получение комментария по ID")
def test_get_comment_by_id(comments_api, created_comment):
    with allure.step(f"Получение комментария {created_comment['id']}"):
        response = comments_api.get_by_id(created_comment["id"])
        assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"]

@allure.feature("Комментарии")
@allure.story("Обновление комментария")
def test_update_comment(comments_api, created_comment):
    with allure.step(f"Обновление комментария {created_comment['id']}"):
        response = comments_api.update(created_comment["id"], updated_comment_data)
        assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"]

@allure.feature("Комментарии")
@allure.story("Удаление комментария")
def test_delete_comment(comments_api, created_comment):
    with allure.step(f"Удаление комментария {created_comment['id']}"):
        response = comments_api.delete(created_comment["id"])
        assert response.status_code in (TEST_CONFIGURATION["STATUS_CODE"], TEST_CONFIGURATION["STATUS_CODE_NO_CONTENT"])
