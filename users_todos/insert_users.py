
import psycopg2
import getpass
from psycopg2 import sql

from gen_fake_users import gen_fake_users,gen_fake_todos

DB_NAME='URL_SHORTENER'
DB_USER='postgres'
DB_PASSWORD=getpass.getpass('Enter you Password: ')
DB_HOST='localhost'
DB_PORT='5432'



# def update_urls(urls):
#     try:
#         conn=psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASSWORD,host=DB_HOST,port=DB_PORT)
#         print('Yay Connected!!!')
#         cursor=conn.cursor()

#         for user in users:
#             insert_query='INSERT INTO users(original_url,short_code) VALUES(%s,%s)'
#             cursor.execute(insert_query,url)

#         conn.commit()

#         cursor.close()
#         conn.close()

#         print(f'Successfully added {len(urls)} urls!')

#     except Exception as e:
#         print(f'An error occured:{e}')

# users=gen_fake_users(1000)



