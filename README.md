# Telegram Random Bot

Бот с функциями:
- Подброс монетки
- Генерация случайных чисел

## Установка

1. Клонировать репозиторий:
```bash
git clone https://github.com/your-repo/telegram-random-bot.git
cd telegram-random-bot
```

2. Установить зависимости:
```bash
pip install -r requirements.txt
```

3. Создать файл `.env` и добавить токен бота:
```
TELEGRAM_BOT_TOKEN=ваш_токен_бота
```

## Запуск
```bash
python bot.py
```

## Команды
- `/start` - Начальное приветствие
- `/help` - Справка по командам
- `/coin` - Подбросить монетку
- `/random [min] [max]` - Случайное число в диапазоне