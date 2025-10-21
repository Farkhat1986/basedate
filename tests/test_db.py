from http import HTTPStatus

import allure


@allure.feature("WordPress Posts API")
@allure.story("Черновой пост не виден публично")
def test_draft_post_not_visible(posts_api, draft_post):
    post_id = draft_post.ID

    with allure.step("GET /posts — черновой пост не должен отображаться"):
        resp = posts_api.get("posts")
        assert resp.status_code == HTTPStatus.OK, f"Ожидался статус 200 при запросе списка постов, получен {resp.status_code}"
        ids = [p["id"] for p in resp.json()]
        assert post_id not in ids, f"Черновой пост с ID {post_id} неожиданно отображается в публичном списке"

    with allure.step("GET /posts/{id} без авторизации — 404"):
        resp_single = posts_api.get(f"posts/{post_id}")
        assert resp_single.status_code == HTTPStatus.NOT_FOUND, f"Черновой пост без авторизации должен возвращать 404, получен {resp_single.status_code}"

    with allure.step("GET /posts/{id} с авторизацией — пост доступен"):
        resp_auth = posts_api.get(f"posts/{post_id}", auth=posts_api.session.auth)
        assert resp_auth.status_code == HTTPStatus.OK, f"Авторизованный запрос к черновому посту должен возвращать 200, получен {resp_auth.status_code}"
        data = resp_auth.json()
        assert data["id"] == post_id, f"ID возвращённого поста ({data.get('id')}) не совпадает с ожидаемым ({post_id})"
        assert data["status"] == "draft", f"Статус поста должен быть 'draft', получен '{data.get('status')}'"


@allure.feature("WordPress Posts API")
@allure.story("Приватный пост недоступен публично")
def test_private_post_visibility(posts_api, private_post):
    post_id = private_post.ID

    with allure.step("GET /posts/{id} без авторизации — 404 (рекомендуется WordPress)"):
        resp = posts_api.get(f"posts/{post_id}")
        # WordPress обычно возвращает 404 вместо 401/403 для приватных постов (безопасность)
        assert resp.status_code == HTTPStatus.NOT_FOUND, f"Приватный пост без авторизации должен возвращать 404, получен {resp.status_code}"

    with allure.step("GET /posts/{id} с авторизацией — пост виден"):
        resp_auth = posts_api.get(f"posts/{post_id}", auth=posts_api.session.auth)
        assert resp_auth.status_code == HTTPStatus.OK, f"Авторизованный запрос к приватному посту должен возвращать 200, получен {resp_auth.status_code}"
        data = resp_auth.json()
        assert data["id"] == post_id, f"ID возвращённого поста ({data.get('id')}) не совпадает с ожидаемым ({post_id})"


@allure.feature("WordPress Posts API")
@allure.story("Запланированный пост недоступен до публикации")
def test_future_post_visibility(posts_api, future_post):
    post_id = future_post.ID

    with allure.step("GET /posts — будущий пост не должен отображаться"):
        resp = posts_api.get("posts")
        ids = [p["id"] for p in resp.json()]
        assert post_id not in ids, f"Будущий пост с ID {post_id} неожиданно отображается в публичном списке"

    with allure.step("GET /posts/{id} без авторизации — 404"):
        resp_single = posts_api.get(f"posts/{post_id}")
        assert resp_single.status_code == HTTPStatus.NOT_FOUND, f"Будущий пост без авторизации должен возвращать 404, получен {resp_single.status_code}"

    with allure.step("GET /posts/{id} с авторизацией — пост доступен"):
        resp_auth = posts_api.get(f"posts/{post_id}", auth=posts_api.session.auth)
        assert resp_auth.status_code == HTTPStatus.OK, f"Авторизованный запрос к будущему посту должен возвращать 200, получен {resp_auth.status_code}"
        data = resp_auth.json()
        assert data["status"] == "future", f"Статус поста должен быть 'future', получен '{data.get('status')}'"


@allure.feature("WordPress Comments API")
@allure.story("Неподтверждённый комментарий не отображается публично")
def test_unapproved_comment_not_visible(comments_api, unapproved_comment):
    """
    Проверяет, что комментарий с comment_approved='0' не отображается
    в публичном REST API WordPress
    """
    post_id = unapproved_comment.comment_post_ID
    comment_content = unapproved_comment.comment_content

    with allure.step(f"GET /comments?post={post_id} — неподтверждённый комментарий не должен отображаться"):
        resp = comments_api.get(f"comments?post={post_id}")
        assert resp.status_code == HTTPStatus.OK, f"Ожидался статус 200 при запросе комментариев, получен {resp.status_code}"

        rendered_comments = [c["content"]["rendered"] for c in resp.json()]
        full_content = " ".join(rendered_comments)

        assert comment_content not in full_content, f"Неподтверждённый комментарий '{comment_content}' неожиданно отображается в публичном API"