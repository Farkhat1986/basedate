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
