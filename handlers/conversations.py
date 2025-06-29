"""
Обработчики диалогов (ConversationHandler)
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from utils.storage import (
    set_user_date, set_user_notification, remove_user_notification,
    has_user_date, get_user_date, get_user_notification
)
from utils.time_utils import parse_date, parse_time, is_date_in_future, is_date_passed

logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
WAITING_FOR_DATE = 1
WAITING_FOR_NOTIFICATION_TIME = 2


async def start_set_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало процесса установки даты (entry point)"""
    await update.message.reply_text(
        "📅 Введите дату в формате ДД.ММ.ГГГГ\n"
        "Например: 25.12.2024\n\n"
        "Или нажмите кнопку для отмены:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Отмена", callback_data="cancel")]
        ])
    )
    return WAITING_FOR_DATE


async def start_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало процесса настройки уведомлений (entry point)"""
    user_id = update.message.from_user.id
    
    if not has_user_date(user_id):
        await update.message.reply_text(
            "❌ Сначала установите дату с помощью команды /set_date!"
        )
        return ConversationHandler.END
    
    current_notification = get_user_notification(user_id) or "Не настроено"
    
    await update.message.reply_text(
        f"🔔 Настройка уведомлений\n\n"
        f"Текущее время уведомлений: {current_notification}\n\n"
        f"Введите время для ежедневных уведомлений в формате ЧЧ:ММ (московское время)\n"
        f"Например: 09:00 или 18:30\n\n"
        f"Или введите 'отключить' чтобы отключить уведомления:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Отмена", callback_data="cancel")]
        ])
    )
    return WAITING_FOR_NOTIFICATION_TIME


async def process_date_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка введенной даты"""
    if not update.message:
        return ConversationHandler.END
        
    user_id = update.message.from_user.id
    date_text = update.message.text.strip()
    
    try:
        # Парсим дату
        target_date = parse_date(date_text)
        
        # Проверяем, что дата в будущем
        if not is_date_in_future(target_date):
            await update.message.reply_text(
                "❌ Дата должна быть в будущем! Попробуйте еще раз или нажмите отмену:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("❌ Отмена", callback_data="cancel")]
                ])
            )
            return WAITING_FOR_DATE
        
        # Сохраняем дату для пользователя
        set_user_date(user_id, target_date)
        
        # Создаем клавиатуру с опциями
        keyboard = [
            [InlineKeyboardButton("⏰ Настроить уведомления", callback_data="setup_notifications")],
            [InlineKeyboardButton("⏰ Показать время", callback_data="show_time")]
        ]
        
        await update.message.reply_text(
            f"✅ Дата успешно установлена: {target_date.strftime('%d.%m.%Y')}\n\n"
            f"Теперь используйте команду /time_left чтобы узнать оставшееся время!\n"
            f"Или настройте уведомления для ежедневных напоминаний.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        return ConversationHandler.END
        
    except ValueError:
        await update.message.reply_text(
            "❌ Неверный формат даты! Используйте формат ДД.ММ.ГГГГ\n"
            "Например: 25.12.2024\n\n"
            "Попробуйте еще раз или нажмите отмену:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Отмена", callback_data="cancel")]
            ])
        )
        return WAITING_FOR_DATE


async def process_notification_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка введенного времени уведомлений"""
    if not update.message:
        return ConversationHandler.END
        
    user_id = update.message.from_user.id
    time_text = update.message.text.strip().lower()
    
    if time_text == "отключить":
        # Отключаем уведомления
        remove_user_notification(user_id)
        
        await update.message.reply_text(
            "🔕 Уведомления отключены!"
        )
        return ConversationHandler.END
    
    try:
        # Парсим время
        notification_time = parse_time(time_text)
        
        # Сохраняем настройки уведомлений
        set_user_notification(user_id, time_text)
        
        # Настраиваем задачу в планировщике
        from services.scheduler_service import setup_notification_job
        setup_notification_job(user_id, notification_time.hour, notification_time.minute)
        
        target_date = get_user_date(user_id)
        
        await update.message.reply_text(
            f"✅ Уведомления настроены на {time_text} каждый день (московское время)!\n\n"
            f"Бот будет присылать вам оставшееся время до {target_date.strftime('%d.%m.%Y')} в это время."
        )
        
        return ConversationHandler.END
        
    except ValueError:
        await update.message.reply_text(
            "❌ Неверный формат времени! Используйте формат ЧЧ:ММ (московское время)\n"
            "Например: 09:00 или 18:30\n\n"
            "Попробуйте еще раз или нажмите отмену:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Отмена", callback_data="cancel")]
            ])
        )
        return WAITING_FOR_NOTIFICATION_TIME


async def conversation_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик нажатий на кнопки внутри ConversationHandler"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "cancel":
        await query.edit_message_text("❌ Операция отменена.")
        return ConversationHandler.END
    elif query.data == "show_time":
        await query.edit_message_text("⏰ Используйте команду /time_left для просмотра оставшегося времени!")
        return ConversationHandler.END
    elif query.data == "setup_notifications":
        await query.edit_message_text("🔔 Используйте команду /notifications для настройки уведомлений!")
        return ConversationHandler.END
    
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена операции"""
    await update.message.reply_text("❌ Операция отменена.")
    return ConversationHandler.END 