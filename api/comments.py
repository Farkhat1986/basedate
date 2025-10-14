<<<<<<< HEAD
from api.base import BaseApi

class CommentsApi(BaseApi):
    """
    Клиент для работы с комментариями через WordPress REST API (эндпоинт /wp/v2/comments)

    Позволяет создавать, получать, обновлять и удалять комментарии.
    По умолчанию использует стандартный префикс WP REST API: 'wp-json/wp/v2'
    """

    def __init__(self, base_url, prefix="wp-json/wp/v2", auth=None, headers=None):
        super().__init__(base_url, prefix, auth, headers)

    def create(self, data):
        """
        Создаёт новый комментарий
        """
        return self.post("comments", json=data)

    def get_by_id(self, comment_id):
        """
        Получает комментарий по его ID.
        """
        return self.get(f"comments/{comment_id}")

    def update(self, comment_id, data):
        """
        Обновляет существующий комментарий
        """
        return self.put(f"comments/{comment_id}", json=data)

    def delete(self, comment_id):
        """
        Удаляет комментарий по ID
        """
        return self.delete(f"comments/{comment_id}")
=======
from config.settings import BASE_URL, API_PREFIX, AUTH, HEADERS
from api.base import BaseApi

class CommentsApi(BaseApi):
    def __init__(self):
        super().__init__(BASE_URL, API_PREFIX, AUTH, HEADERS)

    def create(self, data):
        return self.post("comments", json=data)

    def get_all(self):
        return self.get("comments")

    def get_by_id(self, comment_id):
        return self.get(f"comments/{comment_id}")

    def update(self, comment_id, data):
        return self.post(f"comments/{comment_id}", json=data)

    def delete(self, comment_id):
        return self.delete(f"comments/{comment_id}")
>>>>>>> origin/d1_add_autotests_for_wp
