"""
Фикстуры и тестовые данные для интеграционных тестов WordPress API.

Содержит:
- dataclass для удобного формирования тестовых данных (постов и комментариев)
- сессионные фикстуры для клиентов PostsApi и CommentsApi
- гибкие фикстуры с автоматическим созданием и удалением постов и комментариев
- все фикстуры используют учётные данные и базовый URL из конфигурации
"""

from dataclasses import dataclass
from http import HTTPStatus

import pytest

from api.comments import CommentsApi
from api.posts import PostsApi
from config.settings import TEST_CONFIGURATION
from db.db_connection import get_session
from db.models import Comment, Post
from utils.generators import random_text
from utils.helpers import future_date


@dataclass
class PostData:
    title: str
    content: str
    status: str = "publish"


@dataclass
class CommentData:
    post_id: int
    content: str
    author: str = "TestUser"
    approved: str = "1"


@pytest.fixture(scope="session")
def posts_api():
    """Клиент для работы с постами (сессионная фикстура)"""
    base_url = TEST_CONFIGURATION["BASE_URL"]
    auth = (TEST_CONFIGURATION["WP_USER"], TEST_CONFIGURATION["WP_PASS"])
    return PostsApi(base_url, auth=auth)


@pytest.fixture(scope="session")
def comments_api():
    """Клиент для работы с комментариями"""
    base_url = TEST_CONFIGURATION["BASE_URL"]
    auth = (TEST_CONFIGURATION["WP_USER"], TEST_CONFIGURATION["WP_PASS"])
    return CommentsApi(base_url, auth=auth)


@pytest.fixture
def db_session():
    """Обеспечивает сессию БД для фикстур"""
    with get_session() as session:
        yield session


@pytest.fixture
def created_post(posts_api):
    """Создаёт пост через API с рандомными данными и удаляет после теста"""
    post_data = PostData(
        title=random_text("Тест пост"), content=random_text("Содержимое поста", 20)
    )
    response = posts_api.create(post_data.__dict__)
    assert response.status_code == HTTPStatus.CREATED
    post = response.json()
    yield post
    posts_api.delete_post(post["id"])


@pytest.fixture
def draft_post(db_session):
    """Создаёт черновой пост в БД, возвращает объект и удаляет после теста"""
    post = Post(
        post_title=random_text("Черновой пост"),
        post_content=random_text("Контент черновика", 20),
        post_status="draft",
        post_type="post",
    )
    db_session.add(post)
    db_session.flush()
    yield post
    db_session.delete(post)


@pytest.fixture
def private_post(db_session):
    """Создаёт приватный пост в БД и удаляет после теста"""
    post = Post(
        post_title=random_text("Приватный пост"),
        post_content=random_text("Скрытый контент", 20),
        post_status="private",
        post_type="post",
    )
    db_session.add(post)
    db_session.flush()
    yield post
    db_session.delete(post)


@pytest.fixture
def future_post(db_session):
    """Создаёт будущий пост в БД и удаляет после теста"""
    post = Post(
        post_title=random_text("Будущий пост"),
        post_content=random_text("Контент будущего поста", 20),
        post_status="future",
        post_type="post",
        post_date=future_date(),
    )
    db_session.add(post)
    db_session.flush()
    yield post
    db_session.delete(post)


@pytest.fixture
def created_comment(comments_api, created_post):
    """Создаёт комментарий к существующему посту и удаляет после теста"""
    comment_data = CommentData(
        post_id=created_post["id"], content=random_text("Тестовый комментарий", 12)
    )
    response = comments_api.create(
        {
            "post": comment_data.post_id,
            "author_name": comment_data.author,
            "content": comment_data.content,
            "status": "approve",
        }
    )
    assert response.status_code == HTTPStatus.CREATED
    comment = response.json()
    yield comment
    comments_api.delete(comment["id"])


@pytest.fixture
def unapproved_comment(db_session, draft_post):
    """Создаёт комментарий с comment_approved=0 и удаляет после теста"""
    comment = Comment(
        comment_post_ID=draft_post.ID,
        comment_content=random_text("Комментарий на модерации", 12),
        comment_author="TestUser",
        comment_approved="0",
    )
    db_session.add(comment)
    db_session.flush()
    yield comment
    db_session.delete(comment)
