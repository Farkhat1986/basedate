"""
Модуль для прямого доступа к базе данных WordPress через ORM (SQLAlchemy)
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from db.models import Post, Comment

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


@contextmanager
def get_session():
    """
    Контекстный менеджер для получения сессии базы данных

    Автоматически закрывает сессию после выхода из блока with
    даже если произошло исключение
    """
    session = Session()
    try:
        yield session
    finally:
        session.close()


def get_post_from_db(post_id):
    """Получает пост из таблицы wp_posts по его ID ORM"""
    with get_session() as session:
        stmt = select(Post).where(Post.ID == post_id)
        post = session.execute(stmt).scalar_one_or_none()
        return post


def get_comment_from_db(comment_id):
    """Получает комментарий из таблицы wp_comments по его ID ORM"""
    with get_session() as session:
        stmt = select(Comment).where(Comment.comment_ID == comment_id)
        comment = session.execute(stmt).scalar_one_or_none()
        return comment

