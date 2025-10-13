import os
import base64
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
API_PREFIX = "/wp-json/wp/v2"

AUTH_USER = os.getenv("WP_USER")
AUTH_PASS = os.getenv("WP_PASS")

AUTH = (AUTH_USER, AUTH_PASS)
AUTH_VALUE = base64.b64encode(f"{AUTH_USER}:{AUTH_PASS}".encode()).decode()

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {AUTH_VALUE}"
}

TEST_CONFIGURATION = {
    "TIME_OUT": 10,
    "STATUS_CODE": 200,
    "STATUS_CODE_FIRST": 201,
    "STATUS_CODE_NOT_FOUND": 404,
    "STATUS_CODE_UNAUTHORIZED": 401,
    "STATUS_CODE_ACCEPTED": 202,
    "STATUS_CODE_NO_CONTENT": 204,
}
