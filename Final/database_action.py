

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
       update users set id=? where lower(emporusername)=?
    """, (id, username.lower()))
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

def insert_user(username,code):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
       INSERT INTO users (emporusername, code) VALUES (?, ?)
    """, (username,code))
    conn.commit()
    conn.close()

def delete_user(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
       DELETE from users where lower(emporusername)= ?
    """, (username.lower(),))
    conn.commit()
    conn.close()

def clear_details_update_id(username,new_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
       update users set dateCreated=?, joined=?, id=? where lower(emporusername)=?
    """, (None,0,new_id,username.lower()))
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
    cursor.execute("SELECT joined FROM users WHERE lower(emporusername) = ? and lower(code)= ?", (username.lower(),code.lower()))
    result = cursor.fetchone()
    conn.close()
    allow=True if result else False
    joined = result[0]==1 if result else False
    return allow,joined

def exist_user_code(username,code)-> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE lower(emporusername) = ? and lower(code)= ?", (username.lower(),code.lower()))
    result = cursor.fetchone()
    conn.close()
    return True if result else False

def get_register_id(username)-> int:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE lower(emporusername) = ?", (username.lower(),))
    result = cursor.fetchone()
    conn.close()
    if result and result[0]: 
        return int(result[0])  
    else:  
        return 0
    
def get_all_username_in_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT emporusername FROM users")
    result = cursor.fetchall()
    conn.close()
    return [str(row[0]) for row in result]