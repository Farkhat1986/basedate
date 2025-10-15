import allure
from config.settings import TEST_CONFIGURATION
from db.db_connection import get_post_from_db
from data.data_posts import updated_data

@allure.feature("WordPress Posts API")
@allure.story("Создание нового поста авторизованным пользователем")
def test_create_post(posts_api):
    with allure.step("Создание поста через API"):
        response = posts_api.create({
            "title": "Тест пост",
            "content": "Содержимое поста",
            "status": "publish"
        })
    with allure.step("Проверка ответа"):
        assert response.status_code == TEST_CONFIGURATION["STATUS_CODE_FIRST"]
        post = response.json()
        post_id = post["id"]

    with allure.step("Проверка данных в БД"):
        db_post = get_post_from_db(post_id)
        assert db_post is not None
        assert db_post.post_status == "publish"

@allure.feature("WordPress Posts API")
@allure.story("Получение данных поста по его ID")
def test_get_post_by_id(posts_api, created_post):
    with allure.step(f"Получение поста {created_post['id']}"):
        response = posts_api.get_by_id(created_post["id"])
        assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"]

@allure.feature("WordPress Posts API")
@allure.story("Обновление опубликованного поста")
def test_update_post(posts_api, created_post):
    with allure.step(f"Обновление поста {created_post['id']}"):
        response = posts_api.update(created_post["id"], updated_data)
        assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"]

@allure.feature("WordPress Posts API")
@allure.story("Удаление поста авторизованным пользователем")
def test_delete_post(posts_api, created_post):
    with allure.step(f"Удаление поста {created_post['id']}"):
        response = posts_api.delete_post(created_post["id"])
        assert response.status_code in (
            TEST_CONFIGURATION["STATUS_CODE"],
            TEST_CONFIGURATION["STATUS_CODE_NO_CONTENT"]
        )

