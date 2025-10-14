<<<<<<< HEAD
"""
Фикстуры и тестовые данные для интеграционных тестов WordPress API.

Содержит:
- dataclass для удобного формирования тестовых данных (постов и комментариев),
- сессионные фикстуры для клиентов PostsApi и CommentsApi,
- фикстуры с автоматическим созданием и удалением постов и комментариев

Все фикстуры используют учётные данные и базовый URL из конфигурации
Ресурсы (посты, комментарии) автоматически удаляются после завершения теста
"""

from dataclasses import dataclass
import pytest
from api.comments import CommentsApi
from api.posts import PostsApi
from config.settings import TEST_CONFIGURATION


@dataclass
class CommentData:
    """Тестовые данные для создания комментария"""
    post: int
    content: str


@dataclass
class PostData:
    """Тестовые данные для создания поста"""
    title: str
    content: str
    status: str


@pytest.fixture(scope="session")
def posts_api():
    """Фикстура: клиент для работы с постами (сессионная, создаётся один раз за сессию)"""
    base_url = TEST_CONFIGURATION["BASE_URL"]
    auth = (TEST_CONFIGURATION["WP_USER"], TEST_CONFIGURATION["WP_PASS"])
    return PostsApi(base_url, auth=auth)


@pytest.fixture(scope="session")
def comments_api():
    """Фикстура: клиент для работы с комментариями (сессионная)."""
    base_url = TEST_CONFIGURATION["BASE_URL"]
    auth = (TEST_CONFIGURATION["WP_USER"], TEST_CONFIGURATION["WP_PASS"])
    return CommentsApi(base_url, auth=auth)


@pytest.fixture
def created_comment(comments_api, created_post):
    """
    Фикстура: создаёт комментарий к существующему посту и удаляет его после теста
    """
    comment_data = CommentData(post=created_post["id"], content="Тестовый комментарий")
    response = comments_api.create(comment_data.__dict__)
    assert response.status_code == TEST_CONFIGURATION["STATUS_CODE_FIRST"]
    comment = response.json()
    yield comment

    comments_api.delete(comment["id"])


@pytest.fixture
def created_post(posts_api):
    """
    Фикстура: создаёт опубликованный пост и удаляет его после теста
    """
    post_data = PostData(title="Тест пост", content="Содержимое поста", status="publish")
    response = posts_api.create(post_data.__dict__)
    assert response.status_code == TEST_CONFIGURATION["STATUS_CODE_FIRST"]
    post = response.json()
    yield post

    posts_api.delete(post["id"])
=======
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
>>>>>>> origin/d1_add_autotests_for_wp
