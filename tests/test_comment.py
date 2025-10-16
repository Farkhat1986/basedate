import allure
from db.db_connection import get_comment_from_db
from data.data_comments import updated_comment_data, comment_data
from http import HTTPStatus

@allure.feature("WordPress Comments API")
@allure.story("Создание нового комментария авторизованным пользователем")
def test_create_comment(comments_api, created_post):
    with allure.step(f"Создание комментария для поста {created_post['id']}"):
        response = comments_api.create(comment_data)
        assert response.status_code == HTTPStatus.CREATED
        comment = response.json()

    with allure.step("Проверка комментария в БД"):
        db_comment = get_comment_from_db(comment["id"])
        assert db_comment is not None
        assert db_comment.comment_content == "Тестовый комментарий"

@allure.feature("WordPress Comments API")
@allure.story("Получение данных комментария по его ID")
def test_get_comment_by_id(comments_api, created_comment):
    with allure.step(f"Получение комментария с ID {created_comment['id']}"):
        response = comments_api.get_by_id(created_comment["id"])
        assert response.status_code == HTTPStatus.OK

@allure.feature("WordPress Comments API")
@allure.story("Обновление опубликованного комментария")
def test_update_comment(comments_api, created_comment):
    with allure.step(f"Обновление комментария с ID {created_comment['id']}"):
        response = comments_api.update(created_comment["id"], updated_comment_data)
        assert response.status_code == HTTPStatus.OK

@allure.feature("WordPress Comments API")
@allure.story("Удаление комментария авторизованным пользователем")
def test_delete_comment(comments_api, created_comment):
    with allure.step(f"Удаление комментария с ID {created_comment['id']}"):
        response = comments_api.delete(created_comment["id"])
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)


