

import datetime
import re
import sqlite3
from typing import Optional
from define import DB_NAME

def normalize_phone_number(phone):  
    phone = re.sub(r'[^\d]', '', phone)  
    if phone.startswith('98'): 
        return phone[2:]    
    elif phone.startswith('0'):  
        return phone[1:]  
    else:  
        return phone

def update_id(id, username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
       update users set id=? where emporusername=?
    """, (id, username))
    conn.commit()
    conn.close()

def update_joined(id,joined):
    current=datetime.datetime.now()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
       update users set dateCreated=?, joined=? where id=?
    """, (current,joined,id))
    conn.commit()
    conn.close()

def clear_details_update_id(username,new_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
       update users set dateCreated=?, joined=?, id=? where emporusername=?
    """, (None,0,new_id,username))
    conn.commit()
    conn.close()

def exist_id(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
       select * from users where id=?
    """, (id,))
    result = cursor.fetchone()
    conn.close()
    return True if result else False

def allow_joined_user(username,code)-> Optional[tuple[bool, bool]]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT joined FROM users WHERE emporusername = ? and lower(code)= ?", (username,code.lower()))
    result = cursor.fetchone()
    conn.close()
    allow=True if result else False
    joined = result[0]==1 if result else False
    return allow,joined

def exist_user_code(username,code)-> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE emporusername = ? and lower(code)= ?", (username,code.lower()))
    result = cursor.fetchone()
    conn.close()
    return True if result else False

def get_register_id(username)-> int:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE emporusername = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return int(result[0]) if result else 0

