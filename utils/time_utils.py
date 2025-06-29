"""
Утилиты для работы со временем
"""
from datetime import datetime, timedelta
from typing import Tuple


def calculate_time_left(target_date: datetime) -> Tuple[int, int, int]:
    """
    Вычислить оставшееся время до даты
    
    Returns:
        Tuple[int, int, int]: (дни, часы, минуты)
    """
    now = datetime.now()
    time_diff = target_date - now
    
    days = time_diff.days
    hours = time_diff.seconds // 3600
    minutes = (time_diff.seconds % 3600) // 60
    
    return days, hours, minutes


def format_time_left(days: int, hours: int, minutes: int, target_date: datetime) -> str:
    """
    Форматировать оставшееся время в читаемый вид
    
    Args:
        days: количество дней
        hours: количество часов
        minutes: количество минут
        target_date: целевая дата
        
    Returns:
        str: отформатированная строка времени
    """
    if days > 0:
        time_text = f"📅 До {target_date.strftime('%d.%m.%Y')} осталось:\n\n"
        time_text += f"🕐 {days} дней, {hours} часов, {minutes} минут"
    else:
        time_text = f"📅 До {target_date.strftime('%d.%m.%Y')} осталось:\n\n"
        time_text += f"🕐 {hours} часов, {minutes} минут"
    
    return time_text


def is_date_in_future(date: datetime) -> bool:
    """
    Проверить, что дата в будущем
    
    Args:
        date: проверяемая дата
        
    Returns:
        bool: True если дата в будущем
    """
    return date > datetime.now()


def is_date_passed(date: datetime) -> bool:
    """
    Проверить, что дата уже прошла
    
    Args:
        date: проверяемая дата
        
    Returns:
        bool: True если дата уже прошла
    """
    return date <= datetime.now()


def parse_date(date_text: str) -> datetime:
    """
    Парсить дату из строки формата ДД.ММ.ГГГГ
    
    Args:
        date_text: строка с датой
        
    Returns:
        datetime: объект даты
        
    Raises:
        ValueError: если формат даты неверный
    """
    return datetime.strptime(date_text, "%d.%m.%Y")


def parse_time(time_text: str) -> datetime:
    """
    Парсить время из строки формата ЧЧ:ММ
    
    Args:
        time_text: строка со временем
        
    Returns:
        datetime: объект времени
        
    Raises:
        ValueError: если формат времени неверный
    """
    return datetime.strptime(time_text, "%H:%M") 