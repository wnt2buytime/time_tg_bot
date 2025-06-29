"""
Сервис для работы с планировщиком уведомлений
"""
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from utils.storage import has_user_date, get_user_date, has_user_notification
from utils.time_utils import calculate_time_left, format_time_left, is_date_passed

logger = logging.getLogger(__name__)

# Глобальная переменная для хранения планировщика
scheduler = AsyncIOScheduler()
application = None


def set_application(app):
    """Установить ссылку на приложение для отправки сообщений"""
    global application
    application = app


def start_scheduler():
    """Запустить планировщик"""
    scheduler.start()
    logger.info("Планировщик уведомлений запущен")


def stop_scheduler():
    """Остановить планировщик"""
    scheduler.shutdown()
    logger.info("Планировщик уведомлений остановлен")


def setup_notification_job(user_id: int, hour: int, minute: int) -> None:
    """
    Настроить задачу уведомлений для пользователя
    
    Args:
        user_id: ID пользователя
        hour: час уведомления
        minute: минута уведомления
    """
    job_id = f"notification_{user_id}"
    
    # Удаляем старую задачу если есть
    try:
        scheduler.remove_job(job_id)
    except:
        pass
    
    # Добавляем новую задачу
    scheduler.add_job(
        send_notification,
        CronTrigger(hour=hour, minute=minute),
        id=job_id,
        args=[user_id],
        replace_existing=True
    )
    
    logger.info(f"Уведомления настроены для пользователя {user_id} на время {hour:02d}:{minute:02d}")


def remove_notification_job(user_id: int) -> None:
    """
    Удалить задачу уведомлений для пользователя
    
    Args:
        user_id: ID пользователя
    """
    job_id = f"notification_{user_id}"
    try:
        scheduler.remove_job(job_id)
        logger.info(f"Уведомления удалены для пользователя {user_id}")
    except:
        pass


async def send_notification(user_id: int) -> None:
    """
    Отправить уведомление пользователю
    
    Args:
        user_id: ID пользователя
    """
    try:
        logger.info(f"Попытка отправки уведомления пользователю {user_id}")
        
        if not has_user_date(user_id) or not has_user_notification(user_id):
            logger.warning(f"Пользователь {user_id} не найден в данных")
            return
        
        target_date = get_user_date(user_id)
        
        if is_date_passed(target_date):
            # Дата уже наступила, удаляем задачу
            logger.info(f"Дата для пользователя {user_id} уже наступила, удаляем уведомления")
            remove_notification_job(user_id)
            return
        
        # Вычисляем разность
        days, hours, minutes = calculate_time_left(target_date)
        
        # Формируем сообщение
        notification_text = f"🔔 Ежедневное уведомление!\n\n"
        notification_text += format_time_left(days, hours, minutes, target_date)
        
        # Отправляем уведомление
        if application and application.bot:
            logger.info(f"Отправка уведомления пользователю {user_id}: {notification_text}")
            await application.bot.send_message(chat_id=user_id, text=notification_text)
            logger.info(f"Уведомление успешно отправлено пользователю {user_id}")
        else:
            logger.error(f"Application или bot недоступен для отправки уведомления пользователю {user_id}")
        
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления пользователю {user_id}: {e}") 