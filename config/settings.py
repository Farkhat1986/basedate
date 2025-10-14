import base64

BASE_URL = "http://localhost:8000/wp-json/wp/v2"
AUTH = ("Firstname.LastName", "123-Test")
HEADERS = {"Content-Type": "application/json"}

url_posts = f"{BASE_URL}/posts"
url_comments = f"{BASE_URL}/comments"
auth_value = base64.b64encode(f"{AUTH[0]}:{AUTH[1]}".encode()).decode()
headers_posts = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {auth_value}"
}

TEST_CONFIGURATION = {
    "TEST_POST_ID": 14,
    "TEST_POST_ID_II": 11,
    "TIME_OUT": 10,
    "STATUS_CODE": 200,
    "STATUS_CODE_FIRST": 201,
    "STATUS_CODE_NOT_FOUND": 404,
    "STATUS_CODE_UNAUTHORIZED": 401,
    "STATUS_CODE_ACCEPTED": 202,
    "STATUS_CODE_NO_CONTENT": 204,
    "TEST_COMMENT_ID": 14
}