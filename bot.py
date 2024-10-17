import os
import numpy as np
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# Memuat variabel dari file .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("Token tidak ditemukan! Pastikan variabel lingkungan TELEGRAM_BOT_TOKEN sudah diset.")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Selamat datang! Kirimkan sampel data dengan format '6.8, 7.2, 6.9, ...'")

def calculate_statistics(update: Update, context: CallbackContext) -> None:
    try:
        data = list(map(float, context.args[0].split(',')))
        n = len(data)
        mean = np.mean(data)
        variance = np.var(data, ddof=1)
        std_dev = np.sqrt(variance)
        
        # Format output
        output = f"""
        Count (n): {n}
        Sum (Σx): {sum(data)}
        Mean (x̄): {mean}
        Variance (s²): {variance}
        Standard Deviation (s): {std_dev}
        """
        update.message.reply_text(output)
    except (IndexError, ValueError):
        update.message.reply_text("Format input tidak valid. Pastikan menggunakan format '6.8, 7.2, 6.9, ...'.")

def main() -> None:
    updater = Updater(TOKEN)
    
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, calculate_statistics))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main() 
