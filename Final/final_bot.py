import datetime
import html
from typing import Optional
from telegram import  ChatMember, ChatMemberUpdated, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters,ChatMemberHandler
from invite_private import create_temp_invite_link
from database_action import get_code, is_joined, normalize_phone_number, update_id
from define import CHAT_ID, TOKEN


# async def check_group_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     try:
        
#         async for member in context.bot.get_chat_members(CHAT_ID):  
#         chat_members = await context.bot.get_chat_administrators(chat_id=CHAT_ID)
#         unauthorized_users = []
#         now = datetime.datetime.now()
#         until_date = now + datetime.timedelta(days=1,hours=-1)  
#         until_timestamp = int(until_date.timestamp())
#         for member in chat_members:
#             print(member.user.first_name)
#             print(member.user.last_name)
#             print(member.user.id)
#             if member.status not in ["administrator", "creator"]:
#                 user_id = member.user.id
#                 # if user_id not in AUTHORIZED_USERS:
#                 unauthorized_users.append(user_id)
#                 print(member.user.first_name)
#                 print(member.user.last_name)
#                 print(member.user.id)
#                 await context.bot.ban_chat_member(chat_id=CHAT_ID, user_id=user_id, until_date=until_timestamp)
#                     # await context.bot.unban_chat_member(chat_id=CHAT_ID, user_id=user_id) 
#                 print(f"User {user_id} has been removed.")

#         if unauthorized_users:
#             await update.message.reply_text(f"{len(unauthorized_users)} کاربران غیرمجاز حذف شدند.")
#         else:
#             await update.message.reply_text("همه کاربران مجاز هستند.")
#     except Exception as e:
#         print(f"Error: {e}")
#         await update.message.reply_text("خطایی رخ داد.")

async def request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(text="لطفا شماره موبایل خود را وارد نمایید:")
    context.user_data['step'] = 1

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.clear()
    await update.message.reply_text(text="قوانین به شرح ذیل است:\n\n")
async def handle_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input=update.message.text
    if context.user_data['step'] == 1:
        contact = normalize_phone_number(user_input)
        if contact:
            code= get_code(contact)
            if code != None:
                await update.message.reply_text("🔑 برای ادامه کد اختصاصی خود را وارد نمایید:")
                context.user_data["code"]=code
                context.user_data["phone"]=contact
                context.user_data['step'] = 2
            else:
                await update.message.reply_text(
                        f"شماره موبایل وارد شده در لیست مجاز ما نیست."
                    )
        else:
            await update.message.reply_text(
                        f"لطفا مقادیر صحیح ارسال نمایید"
                    )
    elif context.user_data['step'] == 2:
        if user_input.lower() == str(context.user_data["code"]).lower():
            update_id(update.message.from_user.id, context.user_data["phone"])
            bot = context.bot
            if is_joined(update.message.from_user.id)==False:
                temp_link = await create_temp_invite_link(bot)
                photo_path = "img/join-us.jpg"
                if update.message:
                    await context.bot.send_photo(
                        chat_id=update.message.chat_id,
                        photo=open(photo_path, "rb"),
                        caption=f"کد صحیح است! 🎉\nاین لینک فقط برای شما معتبر است و ظرف 5 دقیقه منقضی می‌شود:\n\n{temp_link}",
                        parse_mode="Markdown",
                    )
            else:
                await update.message.reply_text(
                            f"شما قبلا عضو کانال شده اید."
                        )
        else:  
            await update.message.reply_text("کد نادرست است. لطفاً دوباره امتحان کنید.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    description = (
        "📢 **خوش آمدید!**\n\n"
        "برای ثبت درخواست عضویت در کانال 👇 \n\n"
        "/joinrequest\n\n"
        "همچنین از طریق دکمه منو میتوانید گزینه های دیگر را بررسی نمایید\n"

    )
    photo_path = "img/start-bot.png"
    if update.message:
        await context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=open(photo_path, "rb"),
            caption=description,
            parse_mode="Markdown",
        )
def extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[tuple[bool, bool]]:
    """Takes a ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
    of the chat and whether the 'new_chat_member' is a member of the chat. Returns None, if
    the status didn't change.
    """
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = old_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    is_member = new_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)

    return was_member, is_member


async def greet_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greets new users in chats and announces when someone leaves"""
    result = extract_status_change(update.chat_member)
    if result is None:
        return

    was_member, is_member = result
    cause_name = update.chat_member.from_user.mention_html()
    member_name = update.chat_member.new_chat_member.user.mention_html()
    member_id=update.chat_member.new_chat_member.user.id
    if not was_member and is_member:
        await context.bot.ban_chat_member(chat_id=CHAT_ID, user_id=member_id, until_date=0)
        await update.effective_chat.send_message(
            f"{member_name} was added by {cause_name}. Welcome!",
            parse_mode="Markdown",
        )
    elif was_member and not is_member:
        await update.effective_chat.send_message(
            f"{member_name} is no longer with us. Thanks a lot, {cause_name} ...",
            parse_mode='Markdown',
        )


async def post_init(application) -> None:
    await application.bot.set_my_commands([
        ('rules', 'قوانین عضویت در کانال'),
        ('joinrequest', 'درخواست عضویت در کانال'),
        
    ])
    await application.bot.set_chat_menu_button()
async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    chat_member = update.chat_member
    user_id = chat_member.new_chat_member.user.id
    print(user_id)
    # if user_id not in AUTHORIZED_USERS:
    #     await context.bot.ban_chat_member(chat_id=chat_member.chat.id, user_id=user_id)
    #     await context.bot.unban_chat_member(chat_id=chat_member.chat.id, user_id=user_id)  # آن‌بن برای جلوگیری از مشکل لینک
    #     print(f"User {user_id} removed for unauthorized access.")
    # else:
    #     print(f"User {user_id} joined successfully.")
def main() -> None:
    application = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('joinrequest', request))
    application.add_handler(CommandHandler('rules', rules))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_options))
    # application.add_handler(ChatMemberHandler(handle_new_member, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()