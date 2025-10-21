import requests


class BaseApi:
    """
    Базовый клиент для взаимодействия с REST API.
    Автоматически формирует полный URL из base_url,
    избегая дублирования слэшей. Поддерживает аутентификацию, кастомные заголовки
    и таймауты для всех запросов.
    """

    def __init__(self, base_url, prefix="", auth=None, headers=None, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.prefix = prefix.strip("/")

        self.session = requests.Session()

        if auth is not None:
            self.session.auth = auth

        if headers is not None:
            self.session.headers.update(headers)

        self.timeout = timeout

    def _build_url(self, endpoint):
        """Собирает полный URL из base_url, prefix и endpoint"""
        endpoint = endpoint.lstrip("/")
        if self.prefix:
            return f"{self.base_url}/{self.prefix}/{endpoint}"
        return f"{self.base_url}/{endpoint}"

    def get(self, endpoint, **kwargs):
        """Выполняет GET-запрос к указанному endpoint"""
        return self.session.get(
            self._build_url(endpoint), timeout=self.timeout, **kwargs
        )

    def post(self, endpoint, json=None, **kwargs):
        """Выполняет POST-запрос с передачей JSON"""
        return self.session.post(
            self._build_url(endpoint), json=json, timeout=self.timeout, **kwargs
        )

    def put(self, endpoint, json=None, **kwargs):
        """Выполняет PUT-запрос с передачей JSON"""
        return self.session.put(
            self._build_url(endpoint), json=json, timeout=self.timeout, **kwargs
        )

    def delete(self, endpoint, **kwargs):
        """Выполняет DELETE-запрос к указанному endpoint"""
        return self.session.delete(
            self._build_url(endpoint), timeout=self.timeout, **kwargs
        )

    def close(self):
        """Закрывает HTTP-сессию и освобождает ресурсы"""
        if hasattr(self, 'session') and self.session:
            self.session.close()
