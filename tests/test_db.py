from datetime import datetime, timedelta
from http import HTTPStatus

import allure

from db.db_connection import get_comment_from_db, get_post_from_db, get_session
from db.models import Comment, Post


@allure.feature("WordPress Posts API")
@allure.story("Пост со статусом draft не виден публично")
def test_draft_post_not_visible(posts_api):
    with allure.step("Создание поста в БД со статусом 'draft'"):
        with get_session() as session:
            post = Post(
                post_title="Черновой пост",
                post_content="Контент черновика",
                post_status="draft",
                post_type="post",
            )
            session.add(post)
            session.flush()
            post_id = post.ID

    with allure.step("GET /posts — пост не должен отображаться"):
        resp_list = posts_api.get("posts")
        assert resp_list.status_code == HTTPStatus.OK
        ids = [p["id"] for p in resp_list.json()]
        assert post_id not in ids, "Черновой пост не должен отображаться в списке"

    with allure.step("GET /posts/{id} без авторизации — 404"):
        resp_single = posts_api.get(f"posts/{post_id}")
        assert resp_single.status_code == HTTPStatus.NOT_FOUND

    with allure.step("Очистка"):
        with get_session() as session:
            db_post = get_post_from_db(post_id)
            if db_post:
                session.delete(db_post)


@allure.feature("WordPress Posts API")
@allure.story("Пост со статусом private недоступен без авторизации")
def test_private_post_visibility(posts_api):
    with allure.step("Создание поста со статусом 'private'"):
        with get_session() as session:
            post = Post(
                post_title="Приватный пост",
                post_content="Скрытый контент",
                post_status="private",
                post_type="post",
            )
            session.add(post)
            session.flush()
            post_id = post.ID

    with allure.step("GET /posts/{id} без авторизации — 401 или 404"):
        resp = posts_api.get(f"posts/{post_id}")
        assert resp.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.NOT_FOUND)

    with allure.step("GET /posts/{id} с авторизацией — пост виден"):
        resp_auth = posts_api.get(f"posts/{post_id}", auth=posts_api.session.auth)
        assert resp_auth.status_code == HTTPStatus.OK
        assert resp_auth.json()["id"] == post_id

    with allure.step("Очистка"):
        with get_session() as session:
            db_post = get_post_from_db(post_id)
            if db_post:
                session.delete(db_post)


@allure.feature("WordPress Posts API")
@allure.story("Запланированный пост недоступен до публикации")
def test_future_post_visibility(posts_api):
    with allure.step("Создание поста со статусом 'future'"):
        future_date = datetime.utcnow() + timedelta(days=1)
        with get_session() as session:
            post = Post(
                post_title="Будущий пост",
                post_content="Контент будущего поста",
                post_status="future",
                post_type="post",
                post_date=future_date,
            )
            session.add(post)
            session.flush()
            post_id = post.ID

    with allure.step("GET /posts — будущий пост не должен быть в списке"):
        resp_list = posts_api.get("posts")
        ids = [p["id"] for p in resp_list.json()]
        assert post_id not in ids

    with allure.step("GET /posts/{id} без авторизации — 404"):
        resp_single = posts_api.get(f"posts/{post_id}")
        assert resp_single.status_code == HTTPStatus.NOT_FOUND

    with allure.step("GET /posts/{id} с авторизацией — пост доступен"):
        resp_auth = posts_api.get(f"posts/{post_id}", auth=posts_api.session.auth)
        assert resp_auth.status_code == HTTPStatus.OK
        assert resp_auth.json()["status"] == "future"

    with allure.step("Очистка"):
        with get_session() as session:
            db_post = get_post_from_db(post_id)
            if db_post:
                session.delete(db_post)


@allure.feature("WordPress Comments API")
@allure.story("Неподтверждённый комментарий не отображается публично")
def test_unapproved_comment_not_visible(comments_api):
    with allure.step("Создание поста для комментариев"):
        with get_session() as session:
            post = Post(
                post_title="Пост для комментариев",
                post_content="Контент",
                post_status="publish",
                post_type="post",
            )
            session.add(post)
            session.flush()
            post_id = post.ID

    with allure.step("Создание комментария с comment_approved=0"):
        with get_session() as session:
            comment = Comment(
                comment_post_ID=post_id,
                comment_content="Комментарий на модерации",
                comment_author="TestUser",
                comment_approved="0",
            )
            session.add(comment)
            session.flush()
            comment_id = comment.comment_ID

    with allure.step("GET /comments?post={id} — комментарий не должен отображаться"):
        resp_list = comments_api.get(f"comments?post={post_id}")
        comments = [c["content"]["rendered"] for c in resp_list.json()]
        assert all("Комментарий на модерации" not in c for c in comments)

    with allure.step("Изменение comment_approved=1 и повторный запрос"):
        with get_session() as session:
            db_comment = get_comment_from_db(comment_id)
            db_comment.comment_approved = "1"
            session.add(db_comment)

        resp_list2 = comments_api.get(f"comments?post={post_id}")
        comments2 = [c["content"]["rendered"] for c in resp_list2.json()]
        assert any("Комментарий на модерации" in c for c in comments2)

    with allure.step("Очистка"):
        with get_session() as session:
            c = get_comment_from_db(comment_id)
            if c:
                session.delete(c)
            p = get_post_from_db(post_id)
            if p:
                session.delete(p)


@allure.feature("WordPress Comments API")
@allure.story("Комментарий с несуществующим post_id обрабатывается корректно")
def test_comment_with_invalid_post_id(comments_api):
    with allure.step("Создание комментария с comment_post_ID=999"):
        with get_session() as session:
            comment = Comment(
                comment_post_ID=999,
                comment_content="Комментарий с битой связью",
                comment_author="Ghost",
                comment_approved="1",
            )
            session.add(comment)
            session.flush()
            comment_id = comment.comment_ID

    with allure.step("GET /comments/{id} — объект комментария возвращается"):
        resp = comments_api.get_by_id(comment_id)
        assert resp.status_code == HTTPStatus.OK
        data = resp.json()
        assert data["post"] == 999, "Поле post должно ссылаться на несуществующий ID"

    with allure.step("Очистка"):
        with get_session() as session:
            c = get_comment_from_db(comment_id)
            if c:
                session.delete(c)


@allure.feature("WordPress Posts API")
@allure.story("Черновой пост доступен владельцу")
def test_draft_post_visible_for_owner(posts_api):
    with allure.step("Создание черновика для пользователя ID=1"):
        with get_session() as session:
            post = Post(
                post_title="Черновик владельца",
                post_content="Контент черновика",
                post_status="draft",
                post_type="post",
            )
            session.add(post)
            session.flush()
            post_id = post.ID

    with allure.step("GET /posts/{id} от имени владельца (авторизован)"):
        resp_auth = posts_api.get(f"posts/{post_id}", auth=posts_api.session.auth)
        assert resp_auth.status_code == HTTPStatus.OK
        data = resp_auth.json()
        assert data["status"] == "draft"
        assert "title" in data
        assert "content" in data

    with allure.step("Очистка"):
        with get_session() as session:
            db_post = get_post_from_db(post_id)
            if db_post:
                session.delete(db_post)
