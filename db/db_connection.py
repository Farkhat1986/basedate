"""
Модуль для прямого доступа к базе данных WordPress через ORM (SQLAlchemy)
"""

import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from db.models import Comment, Post

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


@contextmanager
def get_session():
    """
    Контекстный менеджер для получения сессии базы данных

    Делает commit, если всё прошло успешно
    и rollback, если случилось исключение
    В любом случае закрывает сессию
    """
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_post_from_db(post_id):
    """Получает пост из таблицы wp_posts по его ID ORM"""
    with get_session() as session:
        stmt = select(Post).where(Post.ID == post_id)
        return session.execute(stmt).scalar_one_or_none()


def get_comment_from_db(comment_id):
    """Получает комментарий из таблицы wp_comments по его ID ORM"""
    with get_session() as session:
        stmt = select(Comment).where(Comment.comment_ID == comment_id)
        return session.execute(stmt).scalar_one_or_none()
