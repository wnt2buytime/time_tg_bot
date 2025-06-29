"""
Обработчики команд бота
"""
import logging
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

from utils.storage import user_dates, user_notifications

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    welcome_text = """
🤖 Привет! Я бот для отсчета времени до важных дат.

📅 Доступные команды:
/set_date - Установить дату для отсчета
/time_left - Показать оставшееся время
/notifications - Настроить уведомления
/help - Показать справку

Выберите действие:
    """
    
    # Создаем главную клавиатуру с двумя кнопками
    keyboard = [
        [KeyboardButton("⚙️ Настройки"), KeyboardButton("⏰ Оставшееся время")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = """
📋 Справка по использованию бота:

1️⃣ /set_date - Установить дату для отсчета
   Бот попросит ввести дату в формате ДД.ММ.ГГГГ
   Например: 25.12.2024

2️⃣ /time_left - Показать оставшееся время
   Показывает сколько дней и часов осталось до установленной даты

3️⃣ /notifications - Настроить уведомления
   Установить время ежедневных уведомлений (например: 09:00)
   Или отключить уведомления

4️⃣ /help - Показать эту справку

💡 Совет: Установите дату с помощью /set_date, а затем настройте уведомления!
    """
    await update.message.reply_text(help_text)


async def time_left_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показать оставшееся время до установленной даты (команда)"""
    user_id = update.message.from_user.id
    
    if user_id not in user_dates:
        await update.message.reply_text(
            "❌ Дата не установлена!\n\n"
            "Сначала установите дату с помощью команды /set_date"
        )
        return
    
    target_date = user_dates[user_id]
    now = datetime.now()
    
    if target_date <= now:
        await update.message.reply_text(
            "🎉 Установленная дата уже наступила!\n\n"
            "Установите новую дату с помощью /set_date"
        )
        return
    
    # Вычисляем разность
    time_diff = target_date - now
    
    days = time_diff.days
    hours = time_diff.seconds // 3600
    minutes = (time_diff.seconds % 3600) // 60
    
    # Формируем сообщение
    if days > 0:
        time_text = f"📅 До {target_date.strftime('%d.%m.%Y')} осталось:\n\n"
        time_text += f"🕐 {days} дней, {hours} часов, {minutes} минут"
    else:
        time_text = f"📅 До {target_date.strftime('%d.%m.%Y')} осталось:\n\n"
        time_text += f"🕐 {hours} часов, {minutes} минут"
    
    # Добавляем информацию об уведомлениях
    if user_id in user_notifications:
        time_text += f"\n\n🔔 Уведомления настроены на {user_notifications[user_id]}"
    else:
        time_text += f"\n\n🔕 Уведомления не настроены. Используйте /notifications для настройки."
    
    await update.message.reply_text(time_text) 