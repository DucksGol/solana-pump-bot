# telegram_bot.py

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import json

config = json.load(open("config.json"))

def start(update: Update, context: CallbackContext):
    if update.effective_user.id != config["allowed_user_id"]:
        update.message.reply_text("❌ Доступ запрещён.")
        return
    update.message.reply_text("🟢 Бот запущен.\nДоступные команды:\n/set_wallet\n/set_percent\n/balance\n/stats")

def set_wallet(update: Update, context: CallbackContext):
    if update.effective_user.id != config["allowed_user_id"]:
        return
    new_wallet = ' '.join(context.args)
    config["wallet_address"] = new_wallet
    with open("config.json", "w") as f:
        json.dump(config, f)
    update.message.reply_text(f"✅ Кошелек изменён на: {new_wallet}")

def set_percent(update: Update, context: CallbackContext):
    if update.effective_user.id != config["allowed_user_id"]:
        return
    try:
        percent = int(context.args[0])
        if 0 <= percent <= 100:
            config["withdraw_percent"] = percent
            with open("config.json", "w") as f:
                json.dump(config, f)
            update.message.reply_text(f"✅ Процент вывода установлен: {percent}%")
        else:
            update.message.reply_text("❗ Введите число от 0 до 100.")
    except:
        update.message.reply_text("❗ Использование: /set_percent <value>")

def balance(update: Update, context: CallbackContext):
    update.message.reply_text("💰 Баланс: 1.2 SOL / $240")

def stats(update: Update, context: CallbackContext):
    update.message.reply_text("📊 Прибыль за сегодня: +$750\nСделок: 3")

def run_telegram_bot():
    updater = Updater(config["telegram_token"])
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("set_wallet", set_wallet))
    dp.add_handler(CommandHandler("set_percent", set_percent))
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("stats", stats))

    updater.start_polling()
    updater.idle()
