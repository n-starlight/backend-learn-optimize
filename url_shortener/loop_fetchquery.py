import psycopg2
import getpass
from psycopg2 import sql
import time


DB_NAME='URL_SHORTENER'
DB_USER='postgres'
DB_PASSWORD=getpass.getpass('Enter you Password: ')
DB_HOST='localhost'
DB_PORT='5432'

conn=psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASSWORD,host=DB_HOST,port=DB_PORT)
cursor = conn.cursor()


short_codes = ['h3gYA','M55Bk','19lMh','qgFEO']  


query = "SELECT original_url FROM url_shortener WHERE short_code IN %s;"


start_time = time.time()


for _ in range(1000000):
    cursor.execute(query, (tuple(short_codes),))


end_time = time.time()


print(f"Total time taken for 1 million queries: {end_time - start_time:.2f} seconds")


cursor.close()
conn.close()
