import requests
import re
from config.settings import TEST_CONFIGURATION, url_posts, headers_posts
from data.data_posts import data, updated_data
from db.db_connection import get_post_from_db



def test_create_post():
    response = requests.post(url_posts, json=data, headers=headers_posts)

    assert response.status_code == TEST_CONFIGURATION["STATUS_CODE_FIRST"]
    post_data = response.json()
    post_id = post_data["id"]
    assert post_data["title"]["rendered"] == data["title"]
    clean_content = re.sub(r'<[^>]*>', '', post_data["content"]["rendered"]).strip()
    assert clean_content == data["content"]
    assert post_data["status"] == data["status"]

    db_post = get_post_from_db(post_id)
    assert db_post.post_title == data["title"]
    assert data["content"] in db_post.post_content
    assert db_post.post_status == "publish"
    assert db_post.post_type == "post"


def test_get_post_by_id():
    post_id = TEST_CONFIGURATION["TEST_POST_ID_II"]

    response = requests.get(f"{url_posts}/{post_id}")

    assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"]
    post_data = response.json()
    assert post_data["id"] == post_id
    assert post_data["status"] == data["status"]

    db_post = get_post_from_db(post_id)
    assert db_post is not None
    assert db_post.post_status == data["status"]

def test_get_all_posts():
    response = requests.get(url_posts)

    assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"]

    posts_data = response.json()

    for post_data in posts_data:
        assert "id" in post_data
        assert "title" in post_data
        assert "content" in post_data
        assert post_data["status"] == data["status"]

def test_update_post():
    post_id = TEST_CONFIGURATION["TEST_POST_ID"]

    response = requests.post(f"{url_posts}/{post_id}", json=updated_data, headers=headers_posts)

    assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"]
    post_data = response.json()
    assert post_data["title"]["rendered"] == updated_data["title"]
    assert post_data["content"]["rendered"] == "<p>Новое содержимое обновленного поста</p>\n"

    db_post = get_post_from_db(post_id)
    assert db_post is not None, f"Пост {post_id} не найден в БД!"
    assert db_post.post_title == updated_data["title"]
    assert "Новое содержимое обновленного поста" in db_post.post_content
    assert db_post.post_status == "publish"
    assert db_post.post_type == "post"

def test_delete_post():
    post_id = TEST_CONFIGURATION["TEST_POST_ID_II"]

    response = requests.delete(f"{url_posts}/{post_id}", headers=headers_posts)

    assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"]
    post_data = response.json()
    assert post_data["status"] == "trash"

    db_post = get_post_from_db(post_id)
    assert db_post.post_status == "trash"