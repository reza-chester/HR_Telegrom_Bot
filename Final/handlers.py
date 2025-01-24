
from telegram.ext import  ContextTypes
from telegram.constants import  ParseMode
from telegram import Update

from database_action import  clear_details_update_id, exist_id, exist_user_code, get_register_id, update_id,allow_joined_user, update_joined
from define import CHAT_ID, DB_NAME
from functions import create_temp_invite_link, export_table_to_csv, extract_status_change


async def handle_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input=update.message.text
    user_id=update.message.from_user.id
    
    if 'reqstep' in context.user_data :
        if context.user_data['reqstep'] == 1:
            context.user_data["username"]=user_input.lower()
            await update.message.reply_text("*کد اختصاصی* خود را وارد نمایید",parse_mode=ParseMode.MARKDOWN)
            context.user_data['reqstep'] = 2       
        elif context.user_data['reqstep'] == 2:
            allow,joined=allow_joined_user(context.user_data["username"],user_input)
            if allow :
                if not joined:
                    #check back id
                    back_id = get_register_id(context.user_data["username"])
                    if back_id !=0:
                        await context.bot.ban_chat_member(chat_id=CHAT_ID, user_id=back_id, until_date=0)
                    update_id(user_id, context.user_data["username"])
                    bot = context.bot
                    temp_link = await create_temp_invite_link(bot)
                    photo_path = "img/join-us.jpg"
                    if update.message:
                        await update.message.reply_photo(
                            photo=open(photo_path, "rb"),
                            caption=f"کد صحیح است! 🎉\nاین لینک فقط برای شما معتبر است و ظرف 5 دقیقه منقضی می‌شود:\n\n{temp_link}",
                            parse_mode=ParseMode.HTML,
                        )
                else:
                    await update.message.reply_text(
                                "شما قبلا عضو کانال شده اید.\n"
                                "در صورت تمایل برای تغییر شماره عضویت خود در کانال از دستور زیر اقدام نمایید \n\n"
                                "/replacephone",parse_mode=ParseMode.MARKDOWN
                            )
            else:
                context.user_data.clear()  
                await update.message.reply_text("نام کاربری یا کد اختصاصی صحیح *نیست*.\n\n/joinrequest",parse_mode=ParseMode.MARKDOWN)

    elif 'replacereqstep' in context.user_data :
        if context.user_data['replacereqstep'] == 1:
            context.user_data["username"]=user_input.lower()
            await update.message.reply_text("*کد اختصاصی* خود را وارد نمایید",parse_mode=ParseMode.MARKDOWN)
            context.user_data['replacereqstep'] = 2       
        elif context.user_data['replacereqstep'] == 2:
            exist=exist_user_code(context.user_data["username"],user_input)
            if exist :
                register_id= get_register_id(context.user_data["username"])
                await context.bot.ban_chat_member(chat_id=CHAT_ID, user_id=register_id, until_date=0)
                clear_details_update_id(context.user_data["username"],user_id)
                await context.bot.unban_chat_member(chat_id=CHAT_ID, user_id=user_id)
                bot = context.bot
                temp_link = await create_temp_invite_link(bot)
                photo_path = "img/join-us.jpg"
                if update.message:
                    await update.message.reply_photo(
                            photo=open(photo_path, "rb"),
                            caption=f"کد صحیح است! 🎉\nاین لینک فقط برای شما معتبر است و ظرف 5 دقیقه منقضی می‌شود:\n\n{temp_link}",
                            parse_mode=ParseMode.HTML,
                        )
            else:
                context.user_data.clear()  
                await update.message.reply_text("نام کاربری یا کد اختصاصی صحیح *نیست*.\n\n/replacephone",parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("از طریق گزینه های *منو* درخواست خود را بررسی نمایید.",parse_mode=ParseMode.MARKDOWN)

async def greet_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greets new users in chats and announces when someone leaves"""
    result = extract_status_change(update.chat_member)
    if result is None:
        return

    was_member, is_member = result
    user_id=update.chat_member.from_user.id
    cause_name = update.chat_member.from_user.mention_html()
    member_name = update.chat_member.new_chat_member.user.mention_html()
    if not was_member and is_member:
        if exist_id(user_id):
            update_joined(user_id,1)
        else:
            await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=user_id, until_date=0)
    elif was_member and not is_member:
        update_joined(user_id,0)
        
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  
    query = update.callback_query  
    await query.answer()  # Acknowledge the callback query  

    # Handle different callback data  
    if query.data == '1':  
        csv_file = export_table_to_csv(db_name=DB_NAME, table_name='users')  
        await context.bot.send_document(chat_id=update.effective_message.chat_id, document=csv_file, filename='allUsers.csv')  
        await query.edit_message_text(text="CSV file sent!")  
 
    elif query.data == '2':  
        await query.edit_message_text(text="You selected Option 2!") 