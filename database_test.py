import sqlite3

conn = sqlite3.connect('Final/bot_data.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
result = cursor.fetchall()
conn.close()
headers = result[0]  
records = [dict(zip(headers, record)) for record in result[1:]]  
# Find the code for the given username  
username_to_find = 'hamid.bo'  
code = next((record['code'] for record in records if record['emporusername'] == username_to_find), None)  

print(records)
