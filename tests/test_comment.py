import requests
import re
from config.settings import TEST_CONFIGURATION, url_comments, headers_posts, AUTH
from data.data_comments import comment_data, updated_comment_data
from db.db_connection import get_comment_from_db


# Тест кейс 1: Проверка создания нового комментария к посту
def test_create_comment():
    response = requests.post(
        url_comments,
        json=comment_data,
        headers=headers_posts,
        auth=AUTH
    )

    assert response.status_code == TEST_CONFIGURATION["STATUS_CODE_FIRST"]
    comment_response = response.json()
    comment_id = comment_response["id"]

    assert comment_response["post"] == comment_data["post"]
    clean_content = re.sub(r'<[^>]*>', '', comment_response["content"]["rendered"]).strip()
    assert clean_content == comment_data["content"]
    assert comment_response["status"] == "approved"
    assert comment_response["author_name"] == AUTH[0]

    db_comment = get_comment_from_db(comment_id)
    assert db_comment is not None, f"Комментарий {comment_id} не найден в БД!"
    assert db_comment.comment_post_ID == comment_data["post"]
    assert comment_data["content"] in db_comment.comment_content
    assert db_comment.comment_author == AUTH[0]
    assert db_comment.comment_approved == "1"


# Тест кейс 2: Проверка получения комментария по ID
def test_get_comment_by_id():
    comment_id = TEST_CONFIGURATION["TEST_COMMENT_ID"]

    response = requests.get(f"{url_comments}/{comment_id}")

    assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"]
    comment_response = response.json()
    assert comment_response["id"] == comment_id
    assert comment_response["status"] == "approved"

    db_comment = get_comment_from_db(comment_id)
    db_comment = get_comment_from_db(comment_id)
    assert db_comment is not None
    assert db_comment.comment_approved == "1"


# Тест кейс 3: Проверка получения списка всех комментариев
def test_get_all_comments():
    response = requests.get(url_comments)

    assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"]
    comments_data = response.json()

    for comment in comments_data:
        assert "id" in comment
        assert "post" in comment
        assert "content" in comment
        assert comment["status"] == "approved"


# Тест кейс 4: Проверка обновления существующего комментария
def test_update_comment():
    comment_id = TEST_CONFIGURATION["TEST_COMMENT_ID"]

    response = requests.post(
        f"{url_comments}/{comment_id}",
        json=updated_comment_data,
        headers=headers_posts,
        auth=AUTH
    )

    assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"]
    comment_response = response.json()
    clean_content = re.sub(r'<[^>]*>', '', comment_response["content"]["rendered"]).strip()
    assert clean_content == updated_comment_data["content"]

    db_comment = get_comment_from_db(comment_id)
    assert db_comment is not None
    assert updated_comment_data["content"] in db_comment.comment_content


# Тест кейс 5: Проверка удаления комментария
def test_delete_comment():
    comment_id = TEST_CONFIGURATION["TEST_COMMENT_ID"]

    response = requests.delete(
        f"{url_comments}/{comment_id}",
        headers=headers_posts,
        auth=AUTH
    )

    assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"]
    assert response.json()["status"] == "trash"

    db_comment = get_comment_from_db(comment_id)
    assert db_comment is not None
    assert db_comment.comment_approved == "trash"

