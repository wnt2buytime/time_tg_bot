"""
Обработчики клавиатуры
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from utils.storage import (
    user_dates, user_notifications, has_user_date, get_user_date, 
    get_user_notification, has_user_notification
)
from utils.time_utils import calculate_time_left, format_time_left, is_date_passed

logger = logging.getLogger(__name__)


async def handle_keyboard_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки постоянной клавиатуры"""
    if not update.message:
        return
        
    text = update.message.text
    logger.info(f"Обработка кнопки клавиатуры: '{text}' от пользователя {update.message.from_user.id}")
    
    if text == "⚙️ Настройки":
        await show_settings_keyboard(update, context)
    elif text == "⏰ Оставшееся время":
        await show_time_left_menu(update, context)
    elif text == "🔙 Назад":
        await show_main_keyboard(update, context)
    else:
        logger.warning(f"Неизвестная кнопка: '{text}'")


async def show_settings_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показать клавиатуру настроек"""
    settings_text = """
⚙️ Настройки

Выберите действие:
    """
    
    # Создаем клавиатуру настроек
    keyboard = [
        [KeyboardButton("📅 Установить дату"), KeyboardButton("🔔 Уведомления")],
        [KeyboardButton("🔙 Назад")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    await update.message.reply_text(
        settings_text,
        reply_markup=reply_markup
    )


async def show_main_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показать главную клавиатуру"""
    main_text = """
🤖 Главное меню

Выберите действие:
    """
    
    # Создаем главную клавиатуру
    keyboard = [
        [KeyboardButton("⚙️ Настройки"), KeyboardButton("⏰ Оставшееся время")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    await update.message.reply_text(
        main_text,
        reply_markup=reply_markup
    )


async def show_settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показать меню настроек через текстовое сообщение"""
    user_id = update.message.from_user.id
    
    # Проверяем, установлена ли дата
    if not has_user_date(user_id):
        await update.message.reply_text(
            "❌ Дата не установлена!\n\n"
            "Сначала установите дату с помощью кнопки '📅 Установить дату'"
        )
        return
    
    current_notification = get_user_notification(user_id) or "Не настроено"
    target_date = get_user_date(user_id)
    
    settings_text = f"""
⚙️ Настройки

📅 Установленная дата: {target_date.strftime('%d.%m.%Y')}
🔔 Уведомления: {current_notification}

Используйте кнопки клавиатуры для управления:
• 📅 Установить дату - изменить дату
• 🔔 Уведомления - настроить уведомления
    """
    
    await update.message.reply_text(settings_text)


async def show_time_left_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показать оставшееся время через текстовое сообщение"""
    user_id = update.message.from_user.id
    
    if not has_user_date(user_id):
        await update.message.reply_text(
            "❌ Дата не установлена!\n\n"
            "Сначала установите дату с помощью кнопки '📅 Установить дату'"
        )
        return
    
    target_date = get_user_date(user_id)
    
    if is_date_passed(target_date):
        await update.message.reply_text(
            "🎉 Установленная дата уже наступила!\n\n"
            "Установите новую дату с помощью кнопки '📅 Установить дату'"
        )
        return
    
    # Вычисляем разность
    days, hours, minutes = calculate_time_left(target_date)
    
    # Формируем сообщение
    time_text = format_time_left(days, hours, minutes, target_date)
    
    # Добавляем информацию об уведомлениях
    if has_user_notification(user_id):
        notification_time = get_user_notification(user_id)
        time_text += f"\n\n🔔 Уведомления настроены на {notification_time}"
    else:
        time_text += f"\n\n🔕 Уведомления не настроены. Используйте кнопку '🔔 Уведомления' для настройки."
    
    await update.message.reply_text(time_text)


async def set_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Начало процесса установки даты"""
    logger.info(f"Пользователь {update.message.from_user.id} нажал кнопку '📅 Установить дату'")
    # Импортируем функцию из conversations
    from handlers.conversations import start_set_date
    await start_set_date(update, context)


async def notifications_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Начало процесса настройки уведомлений"""
    # Импортируем функцию из conversations
    from handlers.conversations import start_notifications
    await start_notifications(update, context) 