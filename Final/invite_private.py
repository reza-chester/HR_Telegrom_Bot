import datetime
from define import CHAT_ID

async def create_temp_invite_link(bot):
    now = datetime.datetime.now()
    now_plus_10 = now + datetime.timedelta(minutes = 5,hours=-1)
    invite_link = await bot.create_chat_invite_link(
        chat_id=CHAT_ID,
        expire_date=now_plus_10,  
        member_limit=1  
    )
    return invite_link.invite_link
