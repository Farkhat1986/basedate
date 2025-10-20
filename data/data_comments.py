from utils.generators import random_email, random_text


def default_comment_data(post_id: int):
    return {
        "comment_post_ID": post_id,
        "comment_content": random_text("Комментарий", 15),
        "comment_author": random_text("Автор", 8),
        "comment_approved": 1,
        "comment_author_email": random_email(),
    }


def updated_comment_data():
    return {
        "comment_content": random_text("Обновленный комментарий", 15),
        "comment_approved": 1,
    }
