import pytest
import allure
from api.posts import PostsApi
from api.comments import CommentsApi
from data.data_posts import data as post_data
from data.data_comments import comment_data as comment_data_template

@pytest.fixture(scope="session")
def posts_api():
    return PostsApi()

@pytest.fixture(scope="session")
def comments_api():
    return CommentsApi()

@pytest.fixture
def created_post(posts_api):
    with allure.step("Создание тестового поста"):
        response = posts_api.create(post_data)
        post = response.json()
        yield post
    with allure.step(f"Удаление тестового поста {post['id']}"):
        posts_api.delete_post(post["id"])

@pytest.fixture
def created_comment(comments_api, created_post):
    data = comment_data_template.copy()
    data["post"] = created_post["id"]
    with allure.step("Создание тестового комментария"):
        response = comments_api.create(data)
        comment = response.json()
        yield comment
    with allure.step(f"Удаление тестового комментария {comment['id']}"):
        comments_api.delete(comment["id"])
