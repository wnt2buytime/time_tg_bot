"""
Хранение данных пользователей
"""
from datetime import datetime
from typing import Dict, Optional

# Словари для хранения данных пользователей
user_dates: Dict[int, datetime] = {}
user_notifications: Dict[int, str] = {}


def set_user_date(user_id: int, date: datetime) -> None:
    """Установить дату для пользователя"""
    user_dates[user_id] = date


def get_user_date(user_id: int) -> Optional[datetime]:
    """Получить дату пользователя"""
    return user_dates.get(user_id)


def has_user_date(user_id: int) -> bool:
    """Проверить, есть ли дата у пользователя"""
    return user_id in user_dates


def set_user_notification(user_id: int, notification_time: str) -> None:
    """Установить время уведомлений для пользователя"""
    user_notifications[user_id] = notification_time


def get_user_notification(user_id: int) -> Optional[str]:
    """Получить время уведомлений пользователя"""
    return user_notifications.get(user_id)


def has_user_notification(user_id: int) -> bool:
    """Проверить, есть ли уведомления у пользователя"""
    return user_id in user_notifications


def remove_user_notification(user_id: int) -> None:
    """Удалить уведомления пользователя"""
    if user_id in user_notifications:
        del user_notifications[user_id]


def clear_user_data(user_id: int) -> None:
    """Очистить все данные пользователя"""
    if user_id in user_dates:
        del user_dates[user_id]
    if user_id in user_notifications:
        del user_notifications[user_id] 