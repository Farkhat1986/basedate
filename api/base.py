import requests

class BaseApi:
    def __init__(self, base_url, prefix, auth, headers, timeout=10):
        self.base_url = base_url
        self.prefix = prefix
        self.session = requests.Session()
        self.session.auth = auth
        self.session.headers.update(headers)
        self.timeout = timeout

    def _build_url(self, endpoint):
        return f"{self.base_url}{self.prefix}/{endpoint}"

    def get(self, endpoint):
        return self.session.get(self._build_url(endpoint), timeout=self.timeout)

    def post(self, endpoint, json=None):
        return self.session.post(self._build_url(endpoint), json=json, timeout=self.timeout)

    def put(self, endpoint, json=None):
        return self.session.put(self._build_url(endpoint), json=json, timeout=self.timeout)

    def delete(self, endpoint):
        return self.session.delete(self._build_url(endpoint), timeout=self.timeout)
