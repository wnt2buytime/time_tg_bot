#!/bin/bash

# Проверяем наличие файла .env
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo "📝 Создайте файл .env с содержимым:"
    echo "BOT_TOKEN=your_telegram_bot_token_here"
    echo ""
    echo "🔗 Получите токен у @BotFather в Telegram"
    exit 1
fi

# Проверяем наличие токена
if ! grep -q "BOT_TOKEN=" .env; then
    echo "❌ BOT_TOKEN не найден в файле .env"
    exit 1
fi

# Запускаем бота
echo "🤖 Запуск Telegram бота..."
python3 main.py 