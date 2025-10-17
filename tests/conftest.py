"""
Фикстуры и тестовые данные для интеграционных тестов WordPress API.

Содержит:
- dataclass для удобного формирования тестовых данных (постов и комментариев),
- сессионные фикстуры для клиентов PostsApi и CommentsApi,
- фикстуры с автоматическим созданием и удалением постов и комментариев

Все фикстуры используют учётные данные и базовый URL из конфигурации
Ресурсы (посты, комментарии) автоматически удаляются после завершения теста
"""

import random
import string
from dataclasses import dataclass
from http import HTTPStatus

import pytest

from api.comments import CommentsApi
from api.posts import PostsApi
from config.settings import TEST_CONFIGURATION


def random_text(prefix: str, length: int = 8) -> str:
    """Генерирует строку с рандомными буквами и цифрами"""
    chars = string.ascii_letters + string.digits
    suffix = "".join(random.choice(chars) for _ in range(length))
    return f"{prefix} {suffix}"


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
    """Фикстура: клиент для работы с комментариями"""
    base_url = TEST_CONFIGURATION["BASE_URL"]
    auth = (TEST_CONFIGURATION["WP_USER"], TEST_CONFIGURATION["WP_PASS"])
    return CommentsApi(base_url, auth=auth)


@pytest.fixture
def created_post(posts_api):
    """
    Фикстура: создаёт опубликованный пост с рандомным содержимым и удаляет его после теста
    """
    post_data = PostData(
        title=random_text("Тест пост"),
        content=random_text("Содержимое поста", 20),
        status="publish",
    )

    response = posts_api.create(post_data.__dict__)
    assert response.status_code == HTTPStatus.CREATED
    post = response.json()
    yield post

    posts_api.delete(post["id"])


@pytest.fixture
def created_comment(comments_api, created_post):
    """
    Фикстура: создаёт комментарий к существующему посту с рандомным содержимым и удаляет его после теста
    """
    comment_data = CommentData(
        post=created_post["id"], content=random_text("Тестовый комментарий", 12)
    )

    response = comments_api.create(comment_data.__dict__)
    assert response.status_code == HTTPStatus.CREATED
    comment = response.json()
    yield comment

    comments_api.delete(comment["id"])
