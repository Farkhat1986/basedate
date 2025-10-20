from http import HTTPStatus

import allure



@allure.feature("WordPress Posts API")
@allure.story("Черновой пост не виден публично")
def test_draft_post_not_visible(posts_api, draft_post):
    post_id = draft_post.ID

    with allure.step("GET /posts — черновой пост не должен отображаться"):
        resp = posts_api.get("posts")
        assert resp.status_code == HTTPStatus.OK
        ids = [p["id"] for p in resp.json()]
        assert post_id not in ids

    with allure.step("GET /posts/{id} без авторизации — 404"):
        resp_single = posts_api.get(f"posts/{post_id}")
        assert resp_single.status_code == HTTPStatus.NOT_FOUND

    with allure.step("GET /posts/{id} с авторизацией — пост доступен"):
        resp_auth = posts_api.get(f"posts/{post_id}", auth=posts_api.session.auth)
        assert resp_auth.status_code == HTTPStatus.OK
        assert resp_auth.json()["status"] == "draft"


@allure.feature("WordPress Posts API")
@allure.story("Приватный пост недоступен публично")
def test_private_post_visibility(posts_api, private_post):
    post_id = private_post.ID

    with allure.step("GET /posts/{id} без авторизации — 401 или 404"):
        resp = posts_api.get(f"posts/{post_id}")
        assert resp.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.NOT_FOUND)

    with allure.step("GET /posts/{id} с авторизацией — пост виден"):
        resp_auth = posts_api.get(f"posts/{post_id}", auth=posts_api.session.auth)
        assert resp_auth.status_code == HTTPStatus.OK
        assert resp_auth.json()["id"] == post_id


@allure.feature("WordPress Posts API")
@allure.story("Запланированный пост недоступен до публикации")
def test_future_post_visibility(posts_api, future_post):
    post_id = future_post.ID

    with allure.step("GET /posts — будущий пост не должен отображаться"):
        resp = posts_api.get("posts")
        ids = [p["id"] for p in resp.json()]
        assert post_id not in ids

    with allure.step("GET /posts/{id} без авторизации — 404"):
        resp_single = posts_api.get(f"posts/{post_id}")
        assert resp_single.status_code == HTTPStatus.NOT_FOUND

    with allure.step("GET /posts/{id} с авторизацией — пост доступен"):
        resp_auth = posts_api.get(f"posts/{post_id}", auth=posts_api.session.auth)
        assert resp_auth.status_code == HTTPStatus.OK
        assert resp_auth.json()["status"] == "future"


@allure.feature("WordPress Comments API")
@allure.story("Неподтверждённый комментарий не отображается публично")
def test_unapproved_comment_not_visible(comments_api, created_comment, posts_api):
    post_id = created_comment.comment_post_ID

    with allure.step("GET /comments?post={id} — комментарий не должен отображаться"):
        resp_list = comments_api.get(f"comments?post={post_id}")
        comments = [c["content"]["rendered"] for c in resp_list.json()]
        assert all(created_comment.comment_content not in c for c in comments)

    with allure.step(
        "Одобряем комментарий и проверяем — комментарий должен отображаться"
    ):
        created_comment.comment_approved = 1
        resp_list2 = comments_api.get(f"comments?post={post_id}")
        comments2 = [c["content"]["rendered"] for c in resp_list2.json()]
        assert any(created_comment.comment_content in c for c in comments2)
