from telegram import   Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters,ChatMemberHandler,CallbackQueryHandler

from define import  TOKEN
from commands_handler import admin_channel, replace_phone, start,request,rules
from handlers import button, handle_options,greet_chat_members
 




async def post_init(application) -> None:
    await application.bot.set_my_commands([
        ('rules', 'قوانین عضویت در کانال'),
        ('joinrequest', 'عضویت در کانال'),
        ('replacephone', 'تغییر شماره تلگرام'),
        
    ])
    await application.bot.set_chat_menu_button()

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('joinrequest', request))
    application.add_handler(CommandHandler('rules', rules))
    application.add_handler(CommandHandler('replacephone', replace_phone))
    application.add_handler(CommandHandler('admin', admin_channel))
    application.add_handler(CallbackQueryHandler(button))  
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_options))
    application.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()