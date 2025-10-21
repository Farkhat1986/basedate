from http import HTTPStatus

import allure

from data.data_comments import updated_comment_data
from db.db_connection import get_comment_from_db


@allure.feature("WordPress Comments API")
@allure.story("Создание нового комментария авторизованным пользователем")
def test_create_comment(comments_api, created_comment):
    comment_id = created_comment.comment_ID

    with allure.step("Проверка комментария в БД"):
        db_comment = get_comment_from_db(comment_id)
        assert db_comment is not None
        assert db_comment.comment_content == created_comment.comment_content


@allure.feature("WordPress Comments API")
@allure.story("Получение данных комментария по его ID")
def test_get_comment_by_id(comments_api, created_comment):
    comment_id = created_comment.comment_ID
    with allure.step(f"Получение комментария {comment_id}"):
        response = comments_api.get_by_id(comment_id)
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["id"] == comment_id


@allure.feature("WordPress Comments API")
@allure.story("Обновление опубликованного комментария")
def test_update_comment(comments_api, created_comment):
    comment_id = created_comment.comment_ID
    with allure.step(f"Обновление комментария {comment_id}"):
        response = comments_api.update(comment_id, updated_comment_data)
        assert response.status_code == HTTPStatus.OK


@allure.feature("WordPress Comments API")
@allure.story("Удаление комментария авторизованным пользователем")
def test_delete_comment(comments_api, created_comment):
    comment_id = created_comment.comment_ID
    with allure.step(f"Удаление комментария {comment_id}"):
        response = comments_api.delete(comment_id)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
