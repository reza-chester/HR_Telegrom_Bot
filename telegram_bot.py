import logging  
import requests  
from telegram import Update  
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext  

# تنظیمات لاگ‌گذاری  
logging.basicConfig(  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  
    level=logging.INFO  
)  
logger = logging.getLogger(__name__)  

API_URL = "https://example.com/api"  # آدرس API که می‌خواهید درخواست بدهید  

def start(update: Update, context: CallbackContext) -> None:  
    #"""خوش آمدگویی به کاربر."""  
    update.message.reply_text('خوش آمدید! لطفاً یک کد را وارد کنید:')  

def handle_message(update: Update, context: CallbackContext) -> None:  
    #"""دریافت کد و ارسال آن به API."""  
    user_code = update.message.text  
    response_message = send_code_to_api(user_code)  
    update.message.reply_text(response_message)  

def send_code_to_api(code: str) -> str:  
    #"""ارسال کد به API و دریافت پاسخ."""  
    try:  
        response = requests.post(API_URL, json={"code": code})  
        response.raise_for_status()  # در صورت بروز خطا، استثنا ایجاد می‌کند  
        return response.text  # پاسخ دریافتی از API  
    except requests.exceptions.RequestException as e:  
        logger.error(f"Error sending code to API: {e}")  
        return "متاسفم، خطایی در ارسال کد به وجود آمد."  

def main() -> None:  
    #"""اجرا کردن بات."""  
    # توکن بات خود را اینجا وارد کنید  
    updater = Updater("7775436060:AAEiPn2RqBbOBTtWjRIj8WJST7xlwxxcB5Q")  

    # دریافت دیسپاچینگ  
    dispatcher = updater.dispatcher  

    # تعریف دستورات و هندرها  
    dispatcher.add_handler(CommandHandler("start", start))  
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))  

    # شروع بات  
    updater.start_polling()  
    
    # توقف بات با فشار دادن Ctrl+C  
    updater.idle()  

if __name__ == '__main__':  
    main()