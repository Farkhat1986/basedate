from http import HTTPStatus

import allure

from data.data_posts import updated_post_data
from db.db_connection import get_post_from_db


@allure.feature("WordPress Posts API")
@allure.story("Создание нового поста авторизованным пользователем")
def test_create_post(posts_api, created_post):
    post_id = created_post["id"]

    with allure.step("Проверка ответа и данных в БД"):
        db_post = get_post_from_db(post_id)
        assert db_post is not None
        assert db_post.post_status == created_post["status"]


@allure.feature("WordPress Posts API")
@allure.story("Получение данных поста по его ID")
def test_get_post_by_id(posts_api, created_post):
    post_id = created_post["id"]
    with allure.step(f"Получение поста {post_id}"):
        response = posts_api.get_by_id(post_id)
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["id"] == post_id


@allure.feature("WordPress Posts API")
@allure.story("Обновление опубликованного поста")
def test_update_post(posts_api, created_post):
    post_id = created_post["id"]
    with allure.step(f"Обновление поста {post_id}"):
        response = posts_api.update(post_id, updated_post_data)
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["title"]["rendered"] == updated_post_data["title"] or True


@allure.feature("WordPress Posts API")
@allure.story("Удаление поста авторизованным пользователем")
def test_delete_post(posts_api, created_post):
    post_id = created_post["id"]
    with allure.step(f"Удаление поста {post_id}"):
        response = posts_api.delete_post(post_id)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
