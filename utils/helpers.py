from datetime import datetime, timedelta


def future_date(days: int = 1) -> datetime:
    """Возвращает дату в будущем через `days` дней"""
    return datetime.utcnow() + timedelta(days=days)
