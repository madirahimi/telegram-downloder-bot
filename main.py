import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک موردنظرتان را بفرستید تا دانلود کنم.")

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"):
        await update.message.reply_text("لطفاً یک لینک معتبر بفرستید.")
        return

    msg = await update.message.reply_text("⏳ در حال پردازش و دریافت فایل...")
    
    ydl_opts = {
        'outtmpl': 'downloaded_media.%(ext)s',
        'max_filesize': 50 * 1024 * 1024,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await msg.edit_text("📤 در حال آپلود به تلگرام...")
        with open(filename, 'rb') as f:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=f)
        
        if os.path.exists(filename):
            os.remove(filename)
        await msg.delete()

    except Exception as e:
        await msg.edit_text("❌ خطا در دانلود یا حجم بالای ۵0 مگابایت.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))
    app.run_polling()
  
