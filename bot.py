import logging
import random
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Загрузка переменных окружения
TOKEN = "7977098044:AAFYGhAaAaK_ru4xgdZnjQTJhUTa6l04pA8"  # Токен из переменных окружения
PORT = int(os.getenv("PORT", 8443))

# Автоматическое определение Webhook URL для Render
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}/" if RENDER_EXTERNAL_URL else None

# Настройка логгирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот-рандомайзер. Используй команды:"
        "\n/coin - подбросить монетку"
        "\n/random - генерация случайного числа"
        "\n/help - помощь"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Доступные команды:\n"
        "/coin - Подбросить монетку\n"
        "/random [min] [max] - Случайное число в диапазоне\n"
        "Пример: /random 1 100"
    )

async def coin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = random.choice(["Орёл", "Решка"])
    await update.message.reply_text(f"Монетка подброшена: {result}!")

async def random_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("Используйте: /random [мин] [макс]")
            return
            
        min_val = int(args[0])
        max_val = int(args[1])
        
        if min_val > max_val:
            min_val, max_val = max_val, min_val
            
        result = random.randint(min_val, max_val)
        await update.message.reply_text(f"Случайное число: {result}")
        
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите целые числа!")

def main() -> None:
    if not TOKEN:
        logger.error("Токен бота не установлен! Укажите переменную окружения TOKEN.")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("coin", coin))
    app.add_handler(CommandHandler("random", random_number))

    if WEBHOOK_URL:
        # Удаляем завершающий слэш для корректного формирования URL
        webhook_url = WEBHOOK_URL.rstrip('/')
        full_webhook_url = f"{webhook_url}/webhook"
        
        logger.info(f"Запуск через вебхук: {full_webhook_url}")
        
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=full_webhook_url,
            url_path="webhook",  # Указываем путь для вебхука
        )
    else:
        logger.info("Запуск в режиме поллинга")
        app.run_polling()

if __name__ == "__main__":
    main()
