#!/bin/bash

# Скрипт для деплоя Telegram Time Bot на сервер

echo "🚀 Начинаем деплой Telegram Time Bot..."

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.8+"
    exit 1
fi

# Проверяем наличие pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 не найден. Установите pip"
    exit 1
fi

# Создаем виртуальное окружение
echo "📦 Создаем виртуальное окружение..."
python3 -m venv venv

# Активируем виртуальное окружение
echo "🔧 Активируем виртуальное окружение..."
source venv/bin/activate

# Обновляем pip
echo "⬆️ Обновляем pip..."
pip install --upgrade pip

# Устанавливаем зависимости
echo "📚 Устанавливаем зависимости..."
pip install -r requirements.txt

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден!"
    echo "📝 Создайте файл .env с содержимым:"
    echo "BOT_TOKEN=your_bot_token_here"
    echo ""
    echo "Замените 'your_bot_token_here' на ваш токен бота"
    exit 1
fi

# Проверяем токен
if ! grep -q "BOT_TOKEN=" .env; then
    echo "❌ BOT_TOKEN не найден в файле .env"
    exit 1
fi

echo "✅ Деплой завершен успешно!"
echo ""
echo "🔧 Для запуска бота используйте:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "🔄 Для настройки автозапуска:"
echo "   1. Отредактируйте time_bot.service"
echo "   2. Скопируйте в /etc/systemd/system/"
echo "   3. Выполните: sudo systemctl enable time_bot"
echo "   4. Запустите: sudo systemctl start time_bot" 