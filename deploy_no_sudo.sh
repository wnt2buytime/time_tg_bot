#!/bin/bash

# Скрипт для деплоя Telegram Time Bot на сервер (без sudo)

echo "🚀 Начинаем деплой Telegram Time Bot (без sudo)..."

# Проверяем наличие Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден!"
    echo ""
    echo "📋 Ручная установка Python3:"
    echo "1. Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip"
    echo "2. CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "3. Или скачайте с python.org"
    exit 1
fi

# Проверяем наличие pip3
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 не найден!"
    echo ""
    echo "📋 Ручная установка pip3:"
    echo "1. Ubuntu/Debian: sudo apt install python3-pip"
    echo "2. CentOS/RHEL: sudo yum install python3-pip"
    echo "3. Или: curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py --user"
    exit 1
fi

# Проверяем версию Python
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "🐍 Версия Python: $PYTHON_VERSION"

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
echo "🔄 Для настройки автозапуска (требует sudo):"
echo "   1. Отредактируйте time_bot.service"
echo "   2. Скопируйте в /etc/systemd/system/"
echo "   3. Выполните: sudo systemctl enable time_bot"
echo "   4. Запустите: sudo systemctl start time_bot"
echo ""
echo "🔄 Альтернативный автозапуск (без sudo):"
echo "   Добавьте в crontab: @reboot cd /path/to/bot && ./run.sh" 