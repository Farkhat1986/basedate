from config.sett import BASE_URL, API_PREFIX, AUTH, HEADERS
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
