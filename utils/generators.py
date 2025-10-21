import random
import string


def random_text(prefix: str = "Тест", length: int = 8) -> str:
    """Генерирует случайный текст с префиксом"""
    chars = string.ascii_letters + string.digits
    suffix = "".join(random.choice(chars) for _ in range(length))
    return f"{prefix} {suffix}"


def random_email(prefix: str = "user") -> str:
    """Генерирует случайный email"""
    domain = "example.com"
    suffix = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(6)
    )
    return f"{prefix}{suffix}@{domain}"
