

import re
import sqlite3
from define import DB_NAME

def normalize_phone_number(phone):  
    phone = re.sub(r'[^\d]', '', phone)  
    if phone.startswith('98'): 
        return phone[2:]    
    elif phone.startswith('0'):  
        return phone[1:]  
    else:  
        return phone

def update_id(id, phone):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
       update users set id=? where phone=?
    """, (id, phone))
    conn.commit()
    conn.close()

def get_code(contact):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT code FROM users WHERE phone = ?", (normalize_phone_number(contact),))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
def is_joined(id)-> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT joined FROM users WHERE id = ? and joined=true", (id,))
    result = cursor.fetchone()
    conn.close()
    return True if result else False