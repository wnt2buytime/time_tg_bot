# 🚀 Деплой Telegram Time Bot на сервер

Подробная инструкция по развертыванию бота на сервере для круглосуточной работы.

## 📋 Требования к серверу

- **ОС:** Ubuntu 20.04+ / Debian 10+ / CentOS 8+
- **Python:** 3.8 или выше
- **RAM:** минимум 512MB
- **Диск:** минимум 1GB свободного места
- **Сеть:** стабильное интернет-соединение

## 🔧 Подготовка сервера

### 1. Обновление системы
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Установка Python и pip
```bash
sudo apt install python3 python3-pip python3-venv -y
```

### 3. Создание пользователя для бота (рекомендуется)
```bash
sudo adduser timebot
sudo usermod -aG sudo timebot
```

## 📦 Установка бота

### 1. Клонирование репозитория
```bash
cd /home/timebot
git clone <your-repository-url> time_bot
cd time_bot
```

### 2. Запуск скрипта деплоя
```bash
chmod +x deploy.sh
./deploy.sh
```

### 3. Настройка токена бота
```bash
cp env_example.txt .env
nano .env
```
Добавьте ваш токен бота:
```
BOT_TOKEN=your_actual_bot_token_here
```

## 🔄 Настройка автозапуска (systemd)

### 1. Редактирование сервис файла
```bash
nano time_bot.service
```

Измените следующие параметры:
- `User=YOUR_USERNAME` → `User=timebot`
- `WorkingDirectory=/path/to/time_bot` → `WorkingDirectory=/home/timebot/time_bot`
- `Environment=PATH=/path/to/time_bot/venv/bin` → `Environment=PATH=/home/timebot/time_bot/venv/bin`
- `ExecStart=/path/to/time_bot/venv/bin/python main.py` → `ExecStart=/home/timebot/time_bot/venv/bin/python main.py`

### 2. Установка сервиса
```bash
sudo cp time_bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable time_bot
sudo systemctl start time_bot
```

### 3. Проверка статуса
```bash
sudo systemctl status time_bot
```

## 🛠️ Управление ботом

### Запуск/остановка
```bash
# Запуск
sudo systemctl start time_bot

# Остановка
sudo systemctl stop time_bot

# Перезапуск
sudo systemctl restart time_bot

# Проверка статуса
sudo systemctl status time_bot
```

### Просмотр логов
```bash
# Все логи
sudo journalctl -u time_bot

# Логи в реальном времени
sudo journalctl -u time_bot -f

# Логи за последний час
sudo journalctl -u time_bot --since "1 hour ago"
```

## 🔒 Безопасность

### 1. Настройка файрвола
```bash
sudo ufw allow ssh
sudo ufw enable
```

### 2. Защита файла .env
```bash
chmod 600 .env
```

### 3. Регулярные обновления
```bash
# Добавьте в crontab для автоматических обновлений
crontab -e
# Добавьте строку:
# 0 2 * * 0 cd /home/timebot/time_bot && git pull && sudo systemctl restart time_bot
```

## 📊 Мониторинг

### 1. Проверка использования ресурсов
```bash
# Использование памяти
ps aux | grep python

# Использование диска
df -h

# Логи системы
dmesg | tail
```

### 2. Настройка мониторинга (опционально)
```bash
# Установка htop для мониторинга
sudo apt install htop -y
htop
```

## 🔧 Устранение неполадок

### Бот не запускается
```bash
# Проверьте логи
sudo journalctl -u time_bot -n 50

# Проверьте токен
cat .env

# Проверьте зависимости
source venv/bin/activate
pip list
```

### Бот падает
```bash
# Проверьте права доступа
ls -la

# Проверьте свободное место
df -h

# Проверьте сеть
ping api.telegram.org
```

### Обновление бота
```bash
cd /home/timebot/time_bot
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart time_bot
```

## 🌐 Альтернативные способы деплоя

### Docker (опционально)
```bash
# Создайте Dockerfile
cat > Dockerfile << EOF
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
EOF

# Сборка и запуск
docker build -t time-bot .
docker run -d --name time-bot --env-file .env time-bot
```

### Heroku (опционально)
```bash
# Установка Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Создание приложения
heroku create your-time-bot
heroku config:set BOT_TOKEN=your_token
git push heroku main
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи: `sudo journalctl -u time_bot`
2. Убедитесь в правильности токена
3. Проверьте интернет-соединение
4. Перезапустите сервис: `sudo systemctl restart time_bot`

## ✅ Чек-лист деплоя

- [ ] Сервер подготовлен (Python 3.8+, pip)
- [ ] Репозиторий склонирован
- [ ] Виртуальное окружение создано
- [ ] Зависимости установлены
- [ ] Файл .env создан с токеном
- [ ] Бот тестируется локально
- [ ] systemd сервис настроен
- [ ] Автозапуск включен
- [ ] Логи проверены
- [ ] Безопасность настроена 