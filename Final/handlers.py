
from telegram.ext import  ContextTypes
from telegram.constants import  ParseMode
from telegram import Update


async def handle_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input=update.message.text
    if context.user_data['reqstep'] == 1:
        context.user_data["username"]=user_input
        await update.message.reply_text("کد اختصاصی* خود را وارد نمایید*",parse_mode=ParseMode.MARKDOWN)
        context.user_data['reqstep'] = 2       
    elif context.user_data['reqstep'] == 2:
        
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
        # await context.bot.ban_chat_member(chat_id=CHAT_ID, user_id=member_id, until_date=0)
        await update.effective_chat.send_message(
            f"{member_name} was added by {cause_name}. Welcome!",
            parse_mode="Markdown",
        )
    elif was_member and not is_member:
        await update.effective_chat.send_message(
            f"{member_name} is no longer with us. Thanks a lot, {cause_name} ...",
            parse_mode='Markdown',
        )
