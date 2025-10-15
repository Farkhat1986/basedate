"""
Модуль для прямого доступа к базе данных WordPress
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os
from dotenv import load_dotenv

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
    """
    Получает пост из таблицы wp_posts по его ID
    """
    with get_session() as session:
        return session.execute(
            text("SELECT ID, post_title, post_content, post_status, post_type FROM wp_posts WHERE ID = :id"),
            {"id": post_id}
        ).fetchone()


def get_comment_from_db(comment_id):
    """
    Получает комментарий из таблицы wp_comments по его ID
    """
    with get_session() as session:
        return session.execute(
            text("""
                SELECT comment_ID, comment_post_ID, comment_content, comment_author, comment_approved
                FROM wp_comments
                WHERE comment_ID = :id
            """),
            {"id": comment_id}
        ).fetchone()
