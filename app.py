async def send_message():
    bot = Bot(token=TOKEN)
    try:
        # ارسال پیام به کانال
        await bot.send_message(chat_id=CHAT_ID, text="Hello from the bot!")
        print("Message sent!")

        # دریافت اطلاعات کانال
        chat = await bot.get_chat(chat_id=CHAT_ID)
        print(f"Chat ID: {chat.id}")

    except Exception as e:
        print(f"Error: {e}")

# اجرای تابع async
asyncio.run(send_message())