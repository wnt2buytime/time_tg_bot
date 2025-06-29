"""
Основной файл Telegram бота для отсчета времени до даты
"""
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from config import BOT_TOKEN
from handlers.commands import start_command, help_command, time_left_command
from handlers.keyboard import handle_keyboard_button
from handlers.conversations import (
    start_set_date, start_notifications, process_date_input, process_notification_time, 
    conversation_button_callback, cancel, WAITING_FOR_DATE, WAITING_FOR_NOTIFICATION_TIME
)
from services.scheduler_service import start_scheduler, set_application

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def setup_handlers(application: Application) -> None:
    """Настройка обработчиков для приложения"""
    
    # Создаем ConversationHandler для установки даты
    from telegram.ext import ConversationHandler
    date_conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("set_date", start_set_date),
            MessageHandler(filters.Regex(r'^📅 Установить дату$'), start_set_date)
        ],
        states={
            WAITING_FOR_DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_date_input),
                CallbackQueryHandler(conversation_button_callback)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    # Создаем ConversationHandler для настройки уведомлений
    notification_conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("notifications", start_notifications),
            MessageHandler(filters.Regex(r'^🔔 Уведомления$'), start_notifications)
        ],
        states={
            WAITING_FOR_NOTIFICATION_TIME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_notification_time),
                CallbackQueryHandler(conversation_button_callback)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("time_left", time_left_command))
    
    # Добавляем обработчики диалогов (должны быть перед общими обработчиками)
    application.add_handler(date_conv_handler)
    application.add_handler(notification_conv_handler)
    
    # Добавляем обработчик для кнопок клавиатуры (только для кнопок, не обрабатываемых ConversationHandler)
    keyboard_filter = filters.Regex(r'^(⚙️ Настройки|⏰ Оставшееся время|🔙 Назад)$')
    application.add_handler(MessageHandler(keyboard_filter, handle_keyboard_button))
    
    # Добавляем обработчик для callback кнопок (в самом конце)
    application.add_handler(CallbackQueryHandler(conversation_button_callback))


def main() -> None:
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Устанавливаем ссылку на приложение в сервисе планировщика
    set_application(application)
    
    # Настраиваем обработчики
    setup_handlers(application)
    
    # Запускаем планировщик
    start_scheduler()
    
    # Запускаем бота
    logger.info("🤖 Бот запущен с поддержкой уведомлений...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main() 