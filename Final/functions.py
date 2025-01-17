import datetime
from typing import Optional
from telegram import ChatMember, ChatMemberUpdated
from define import CHAT_ID


async def unban_users(context):
    users_list_id=[181174595]
    for id in users_list_id:
        await context.bot.unban_chat_member(chat_id=CHAT_ID, user_id=id)
    
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

