import datetime
from io import BytesIO
import sqlite3
import pandas as pd  
from typing import Optional
from telegram import ChatMember, ChatMemberUpdated
from define import CHAT_ID
from telegram.ext import ContextTypes

async def unban_users(context):
    users_list_id=[181174595]
    for id in users_list_id:
        await context.bot.unban_chat_member(chat_id=CHAT_ID, user_id=id)

async def user_joined_chat(context: ContextTypes.DEFAULT_TYPE,user_id):
    try:
       res = await context.bot.get_chat_member(chat_id=CHAT_ID, user_id=user_id)
       if res.status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
        ChatMember.RESTRICTED
        ] : return True
    except Exception as e:
       return False

async def create_temp_invite_link(bot):
    now = datetime.datetime.now()
    now_plus_10 = now + datetime.timedelta(minutes = 5,hours=-1)
    invite_link = await bot.create_chat_invite_link(
        chat_id=CHAT_ID,
        expire_date=now_plus_10,  
        member_limit=1  
    )
    return invite_link.invite_link



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

def export_table_to_csv(db_name: str, table_name: str) -> BytesIO:  
    conn = sqlite3.connect(db_name)  
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)  
    csv_buffer = BytesIO()  
    df.to_csv(csv_buffer, index=False,header=True)  
    csv_buffer.seek(0) 
    conn.close() 
    return csv_buffer  

async def get_user_status_in_channel(bot, channel_id, user_id):  
    try:  
        chat_member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)  
        status = chat_member.status  
        return status    
    except Exception as e:  
        if "User not found" in str(e):  
            return "not_found" 
        elif "Chat not found" in str(e):  
            return "channel_not_found" 
        else:  
            print(f"خطای BadRequest: {e}")  
            return "error" 
    except Exception as e:  
        print(f"خطای غیرمنتظره: {e}")  
        return "error"  
    
# def fetch_users_from_final_excel(excel):
     