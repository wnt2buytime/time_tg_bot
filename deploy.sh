#!/bin/bash

# Скрипт для деплоя Telegram Time Bot на сервер

echo "🚀 Начинаем деплой Telegram Time Bot..."

# Определяем тип системы
if [ -f /etc/debian_version ]; then
    # Debian/Ubuntu
    echo "📦 Обнаружена Debian/Ubuntu система"
    PKG_MANAGER="apt"
    PYTHON_PKG="python3"
    PIP_PKG="python3-pip"
elif [ -f /etc/redhat-release ]; then
    # CentOS/RHEL/Fedora
    echo "📦 Обнаружена CentOS/RHEL/Fedora система"
    PKG_MANAGER="yum"
    PYTHON_PKG="python3"
    PIP_PKG="python3-pip"
else
    echo "❌ Неподдерживаемая система. Установите Python 3.8+ вручную"
    exit 1
fi

# Обновляем пакеты
echo "🔄 Обновляем пакеты..."
sudo $PKG_MANAGER update -y

# Проверяем и устанавливаем Python3
if ! command -v python3 &> /dev/null; then
    echo "📦 Устанавливаем Python3..."
    sudo $PKG_MANAGER install -y $PYTHON_PKG
else
    echo "✅ Python3 уже установлен"
fi

# Проверяем и устанавливаем pip3
if ! command -v pip3 &> /dev/null; then
    echo "📦 Устанавливаем pip3..."
    sudo $PKG_MANAGER install -y $PIP_PKG
else
    echo "✅ pip3 уже установлен"
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
echo "🔄 Для настройки автозапуска:"
echo "   1. Отредактируйте time_bot.service"
echo "   2. Скопируйте в /etc/systemd/system/"
echo "   3. Выполните: sudo systemctl enable time_bot"
echo "   4. Запустите: sudo systemctl start time_bot" 