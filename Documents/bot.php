<?php  

require 'vendor/autoload.php';  

use Longman\TelegramBot\Telegram;  
use Longman\TelegramBot\Request;  

$API_KEY = '7775436060:AAEiPn2RqBbOBTtWjRIj8WJST7xlwxxcB5Q'; // توکن خود را اینجا وارد کنید  
$bot_username = 'rezachester_bot'; // نام کاربری بات خود را اینجا وارد کنید  

$telegram = new Telegram($API_KEY, $bot_username);  

// دریافت درخواست  
$update = $telegram->getWebhookUpdate();  

// بررسی نوع درخواست  
if ($update->getMessage()) {  
    $chat_id = $update->getMessage()->getChat()->getId();  
    $text = $update->getMessage()->getText();  

    // پاسخ به پیام "سلام"  
    if ($text == '/start' || $text == 'سلام') {  
        $reply = 'سلام! خوش آمدید به بات من!';  
        Request::sendMessage(['chat_id' => $chat_id, 'text' => $reply]);  
    }  
}