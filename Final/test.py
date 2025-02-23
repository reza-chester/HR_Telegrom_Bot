from database_action import get_all_username_in_db
from define import DB_NAME
from functions import export_table_to_csv


csv_buffer = export_table_to_csv(DB_NAME, "users")

# چاپ محتوای CSV (برای تست)
print(csv_buffer.getvalue().decode('utf-8'))
