import allure
from config.settings import TEST_CONFIGURATION
from db.db_connection import get_post_from_db
from data.data_posts import updated_data

<<<<<<< HEAD

@allure.feature("WordPress Posts API")
@allure.story("Авторизованный пользователь может создать опубликованный пост")
=======
@allure.feature("Посты")
@allure.story("Создание поста")
>>>>>>> origin/d1_add_autotests_for_wp
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

<<<<<<< HEAD
    with allure.step("Проверка данных в базе данных"):
=======
    with allure.step("Проверка данных в БД"):
>>>>>>> origin/d1_add_autotests_for_wp
        db_post = get_post_from_db(post_id)
        assert db_post is not None
        assert db_post.post_status == "publish"

<<<<<<< HEAD

@allure.feature("WordPress Posts API")
@allure.story("Пользователь может получить данные поста по его ID")
def test_get_post_by_id(posts_api, created_post):
    with allure.step(f"Получение поста с ID {created_post['id']}"):
        response = posts_api.get_by_id(created_post["id"])
        assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"]


@allure.feature("WordPress Posts API")
@allure.story("Авторизованный пользователь может обновить заголовок и содержимое своего поста")
def test_update_post(posts_api, created_post):
    with allure.step(f"Обновление поста с ID {created_post['id']}"):
        response = posts_api.update(created_post["id"], updated_data)
        assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"]


@allure.feature("WordPress Posts API")
@allure.story("Авторизованный пользователь может удалить свой пост")
def test_delete_post(posts_api, created_post):
    with allure.step(f"Удаление поста с ID {created_post['id']}"):
        response = posts_api.delete_post(created_post["id"])
        assert response.status_code in (
            TEST_CONFIGURATION["STATUS_CODE"],
            TEST_CONFIGURATION["STATUS_CODE_NO_CONTENT"]
        )
=======
@allure.feature("Посты")
@allure.story("Получение поста по ID")
def test_get_post_by_id(posts_api, created_post):
    with allure.step(f"Получение поста {created_post['id']}"):
        response = posts_api.get_by_id(created_post["id"])
        assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"]

@allure.feature("Посты")
@allure.story("Обновление поста")
def test_update_post(posts_api, created_post):
    with allure.step(f"Обновление поста {created_post['id']}"):
        response = posts_api.update(created_post["id"], updated_data)
        assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"]

@allure.feature("Посты")
@allure.story("Удаление поста")
def test_delete_post(posts_api, created_post):
    with allure.step(f"Удаление поста {created_post['id']}"):
        response = posts_api.delete_post(created_post["id"])
        assert response.status_code in (TEST_CONFIGURATION["STATUS_CODE"], TEST_CONFIGURATION["STATUS_CODE_NO_CONTENT"])
>>>>>>> origin/d1_add_autotests_for_wp
