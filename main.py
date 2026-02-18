import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# CONFIGURATION
BOT_TOKEN = "8596462322:AAHKSNHZtDCoOpYFwI9iPXI5xhxr6dWvp_4"
BOT_USERNAME = "anime_files123_bot"
CHANNEL_ID = -1003425936815
OWNER_ID = 6657777803
FILE_EXPIRY_MINUTES = 20

# Logging Setup - FIXED
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__) # ✅ Fixed

async def save_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    try:
        sent = await context.bot.copy_message(
            chat_id=CHANNEL_ID,
            from_chat_id=update.effective_chat.id,
            message_id=update.message.message_id,
        )
        file_msg_id = sent.message_id
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Open File", url=f"https://t.me/{BOT_USERNAME}?start={file_msg_id}")]])
        
        await update.message.delete()
        await context.bot.send_message(chat_id=OWNER_ID, text="✅ File saved successfully!")
        await context.bot.send_message(chat_id=OWNER_ID, text=f"🔑 File ID: {file_msg_id}", reply_markup=button)
    except Exception as e:
        logger.error(f"Error: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        msg_id = context.args[0]
        try:
            sent = await context.bot.copy_message(chat_id=update.effective_chat.id, from_chat_id=CHANNEL_ID, message_id=int(msg_id))
            info_msg = await context.bot.send_message(chat_id=update.effective_chat.id, text=f"This video will be deleted after {FILE_EXPIRY_MINUTES} minutes.")
            
            async def delete_task():
                await asyncio.sleep(FILE_EXPIRY_MINUTES * 60)
                try:
                    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=sent.message_id)
                    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=info_msg.message_id)
                except: pass
            
            asyncio.create_task(delete_task())
        except:
            await update.message.reply_text("❌ File not found.")
    else:
        await update.message.reply_text("👋 Send me a File ID to get the file.")

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & (filters.VIDEO | filters.Document.ALL), save_file))
    
    logger.info("🤖 Bot is running...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__": # ✅ Fixed
    asyncio.run(main())
