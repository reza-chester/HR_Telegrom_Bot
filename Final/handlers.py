
import os
import pandas as pd
from telegram.ext import  ContextTypes
from telegram.constants import  ParseMode
from telegram import Update

from commands_handler import start_commands
from database_action import  clear_details_update_id, delete_user, exist_id, exist_user_code, get_all_username_in_db, get_register_id, insert_user, update_id,allow_joined_user, update_joined
from define import CHAT_ID, DB_NAME
from functions import create_temp_invite_link, export_table_to_csv, extract_status_change, get_user_status_in_channel

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     if 'adminupdatefile' in context.user_data :
        file = await update.message.document.get_file()
        temp_file_path = 'temp_file.csv'
        await file.download_to_drive(temp_file_path)
        # try:
        SAVE_DIR = 'saved_files'
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR) 
                
        df = pd.read_csv(temp_file_path)
        list_col=df.columns.tolist()
        if "emporusername" in list_col  and "code" in list_col:
            await update.message.reply_text("File received successfully!")
            await update.message.reply_text(f"Count of rows: {df.shape[0]}")
            final_users=df["emporusername"].tolist()
            all_coding=df["code"].tolist()
            allow_code =True
            for mcode in all_coding:
                if pd.isna(mcode):
                    allow_code=False
                    break
            if allow_code:
                error_username = None
                for chk_usr in final_users:
                    if pd.isna(chk_usr):
                        await update.message.reply_text(f"You have an empty username.")
                        error_username="NULL"
                    elif '@' in chk_usr or '.' not in chk_usr:
                        error_username=chk_usr
                        break
                if error_username is None:
                    old_users=get_all_username_in_db()
                    new_users=[nw_user for nw_user in final_users if nw_user not in old_users]
                    left_user=[lft_user for lft_user in old_users if lft_user not in final_users]
                    await update.message.reply_text(f"Count of new users: {len(new_users)}")
                    await update.message.reply_text(f"Count of users to be kicked from the channel: {len(left_user)}")
                    context.user_data['adminapprove'] = 1
                    permanent_file_path = os.path.join(SAVE_DIR, 'processed_file.csv')
                    df.to_csv(permanent_file_path, index=False)
                    await update.message.reply_text(f"Approved? Yes / No")  
                else:
                    await update.message.reply_text(f"This username is not allowed: {error_username}")
            else:
                await update.message.reply_text(f"You have a user without a code in your file.")
        else:
            await update.message.reply_text("Please check that the header contains 'emporusername' and 'Code'")
            
            
        # except Exception as e:
        #     await update.message.reply_text(f"Error processing the file: {e}")

        # # Delete the temporary file
        # if os.path.exists(temp_file_path):
        #     os.remove(temp_file_path)
        
        
            
async def handle_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input=update.message.text
    user_id=update.message.from_user.id
    
    if 'reqstep' in context.user_data :
        if context.user_data['reqstep'] == 1:
            context.user_data["username"]=user_input.lower()
            await update.message.reply_text("*کد اختصاصی* رو هم بزن.",parse_mode=ParseMode.MARKDOWN)
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
                    await context.bot.unban_chat_member(chat_id=CHAT_ID, user_id=user_id)
                    bot = context.bot
                    temp_link = await create_temp_invite_link(bot)
                    photo_path = "img/join-us.jpg"
                    if update.message:
                        linea="<b> کد تأیید شد! 🎉</b>"
                        await update.message.reply_photo(
                            photo=open(photo_path, "rb"),
                            caption=f"{linea}\n\nاین لینک فقط برای تو معتبره و تا ۵ دقیقه دیگه منقضی می‌شه:\n\n{temp_link}",
                            parse_mode=ParseMode.HTML,
                        )
                else:
                    await update.message.reply_text(
                                "شما قبلا عضو کانال شده اید.\n"
                                "اگه می‌خوای شماره عضویتت رو عوض کنی، از دستور زیر استفاده کن:\n\n"
                                "/replacephone"

                                ,parse_mode=ParseMode.MARKDOWN
                            )
            else:
                context.user_data.clear()  
                await update.message.reply_text("نام کاربری یا کد اختصاصی صحیح نیست.",parse_mode=ParseMode.MARKDOWN)

    elif 'replacereqstep' in context.user_data :
        if context.user_data['replacereqstep'] == 1:
            context.user_data["username"]=user_input.lower()
            await update.message.reply_text("*کد اختصاصی* رو هم بزن.",parse_mode=ParseMode.MARKDOWN)
            context.user_data['replacereqstep'] = 2       
        elif context.user_data['replacereqstep'] == 2:
            exist=exist_user_code(context.user_data["username"],user_input)
            if exist :
                register_id= get_register_id(context.user_data["username"])
                status = await get_user_status_in_channel(context.bot, CHAT_ID, register_id) 
                if status in ["member","restricted"]:
                    await context.bot.ban_chat_member(chat_id=CHAT_ID, user_id=register_id, until_date=0)
                clear_details_update_id(context.user_data["username"],user_id)
                await context.bot.unban_chat_member(chat_id=CHAT_ID, user_id=user_id)
                bot = context.bot
                temp_link = await create_temp_invite_link(bot)
                photo_path = "img/join-us.jpg"
                if update.message:
                    linea="<b> کد تأیید شد! 🎉</b>"
                    await update.message.reply_photo(
                            photo=open(photo_path, "rb"),
                            caption=f"{linea}\n\nاین لینک فقط برای تو معتبره و تا ۵ دقیقه دیگه منقضی می‌شه:\n\n{temp_link}",
                            parse_mode=ParseMode.HTML,
                        )
            else:
                context.user_data.clear()  
                await update.message.reply_text("نام کاربری یا کد اختصاصی صحیح نیست.",parse_mode=ParseMode.MARKDOWN)
    elif 'admincheckuser' in context.user_data :
        register_id= get_register_id(user_input)
        await update.message.reply_text(f"Register ID: {register_id}")
        if register_id!=0:
            status = await get_user_status_in_channel(context.bot, CHAT_ID, register_id) 
            await update.message.reply_text(f"Status: {status}") 
    elif 'adminapprove' in context.user_data:
        if user_input.lower() == 'yes':
            permanent_file_path = os.path.join('saved_files', 'processed_file.csv')
            df = pd.read_csv(permanent_file_path)
            final_users=df["emporusername"].tolist()
            old_users=get_all_username_in_db()
            new_users=[nw_user for nw_user in final_users if nw_user not in old_users]
            left_user=[lft_user for lft_user in old_users if lft_user not in final_users]
            for nw_usa in new_users:
                if len(str(nw_usa)) !=0:
                    code=df[df["emporusername"]==nw_usa]['code'].values[0]
                    insert_user(nw_usa,code)
            for lft_u in left_user:
                register_ids=get_register_id(lft_u)
                if register_ids !=0:
                    status = await get_user_status_in_channel(context.bot, CHAT_ID, register_ids) 
                    if status in ["member","restricted"]:
                        await context.bot.ban_chat_member(chat_id=CHAT_ID, user_id=register_ids, until_date=0)
                delete_user(lft_u)
            
            await update.message.reply_text(f"Your request has been completed. Total number of active users: {len(get_all_username_in_db())}")
        else:
            start_commands(context)
        
       
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
    start_commands(context) 
    query = update.callback_query  
    await query.answer() 
    if query.data == '1':  
        csv_file = export_table_to_csv(db_name=DB_NAME, table_name='users')  
        await context.bot.send_document(chat_id=update.effective_message.chat_id, document=csv_file, filename='allUsers.csv')  
        await query.edit_message_text(text="CSV file sent!")  
 
    elif query.data == '2':
        context.user_data['admincheckuser'] = 1  
        await query.edit_message_text(text="Enter username:") 
    elif query.data == '3':
        csv_file = export_table_to_csv(db_name=DB_NAME, table_name='users')  
        await context.bot.send_document(chat_id=update.effective_message.chat_id, document=csv_file, filename='BackupDB.csv') 
        context.user_data['adminupdatefile'] = 1  
        await query.edit_message_text(text="Keep the backup file with you, please update the final file to record the changes.") 