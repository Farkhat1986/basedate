<<<<<<< HEAD
from api.base import BaseApi


class PostsApi(BaseApi):
    """
    Клиент для работы с WordPress REST API (эндпоинт /wp/v2/posts)

    Предоставляет удобные методы для создания, получения, обновления и удаления постов
    По умолчанию использует префикс 'wp-json/wp/v2', как того требует WP REST API
    """

    def __init__(self, base_url, prefix="wp-json/wp/v2", auth=None, headers=None):
        super().__init__(base_url, prefix, auth, headers)

    def create(self, data):
        """
        Создаёт новый пост в WordPress
        """
        return self.post("posts", json=data)

    def get_by_id(self, post_id):
        """
        Получает пост по его ID
        """
        return self.get(f"posts/{post_id}")

    def update(self, post_id, data):
        """
        Обновляет существующий пост
        """
        return self.put(f"posts/{post_id}", json=data)

    def delete_post(self, post_id, force=True):
        """
        Удаляет пост

        По умолчанию удаляет принудительно (минуя корзину WordPress)
        Если force=False — пост переместится в корзину (если включена)
        """
        return self.delete(f"posts/{post_id}?force={'true' if force else 'false'}")

=======
from config.settings import BASE_URL, API_PREFIX, AUTH, HEADERS
from api.base import BaseApi

class PostsApi(BaseApi):
    def __init__(self):
        super().__init__(BASE_URL, API_PREFIX, AUTH, HEADERS)

    def create(self, data):
        return self.post("posts", json=data)

    def get_all(self):
        return self.get("posts")

    def get_by_id(self, post_id):
        return self.get(f"posts/{post_id}")

    def update(self, post_id, data):
        return self.post(f"posts/{post_id}", json=data)

    def delete_post(self, post_id):
        return self.delete(f"posts/{post_id}")
>>>>>>> origin/d1_add_autotests_for_wp
