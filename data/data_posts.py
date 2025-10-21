from utils.generators import random_text


def default_post_data():
    return {
        "title": random_text("Пост"),
        "content": random_text("Контент", 20),
        "status": "publish",
    }


def updated_post_data():
    return {
        "title": random_text("Обновленный пост"),
        "content": random_text("Обновленный контент", 20),
        "status": "publish",
    }
