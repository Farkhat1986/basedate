from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""


class Post(Base):
    """Модель для таблицы wp_posts"""

    __tablename__ = "wp_posts"

    ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_title: Mapped[str] = mapped_column(String(255))
    post_content: Mapped[str] = mapped_column(Text)
    post_status: Mapped[str] = mapped_column(String(20))
    post_type: Mapped[str] = mapped_column(String(20))
    post_date: Mapped[datetime] = mapped_column(DateTime)

    def __repr__(self):
        return f"<Post {self.ID}: {self.post_title!r}>"


class Comment(Base):
    """Модель для таблицы wp_comments"""

    __tablename__ = "wp_comments"

    comment_ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment_post_ID: Mapped[int] = mapped_column(Integer)
    comment_content: Mapped[str] = mapped_column(Text)
    comment_author: Mapped[str] = mapped_column(String(255))
    comment_approved: Mapped[str] = mapped_column(String(20))

    def __repr__(self):
        return f"<Comment {self.comment_ID}: {self.comment_author!r}>"
