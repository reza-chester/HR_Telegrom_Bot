import sqlite3
DB_NAME = "bot_data.db"


conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (  
    emporusername TEXT PRIMARY KEY UNIQUE,  
    phone TEXT,  
    code TEXT,  
    id INT,
    joined BIT,  
    dateCreated DATETIME  
) 
    """)
conn.commit()
conn.close()



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    # keyboard = [
    #     [InlineKeyboardButton("📥 دانلود ویدیو", callback_data="download_video")],
    #     [InlineKeyboardButton("ℹ️ درباره ما", url="https://example.com")],
    # ]
    # reply_markup = InlineKeyboardMarkup(keyboard)

    description = (
        "📢 **خوش آمدید!**\n\n"
        "به ربات ما خوش آمدید! از طریق دکمه منو درخواست های خود را بررسی نمایید.\n"
    )
    photo_path = "img/start-bot.png"
    if update.message:
        await context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=open(photo_path, "rb"),
            caption=description,
            parse_mode="Markdown",
        )