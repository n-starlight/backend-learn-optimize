
import psycopg2
import getpass
import time
from psycopg2 import sql
import psycopg2.extras

from gen_fakeurls import gen_fakeurls,gen_unique_codes

DB_NAME='URL_SHORTENER'
DB_USER='postgres'
DB_PASSWORD=getpass.getpass('Enter you Password: ')
DB_HOST='localhost'
DB_PORT='5432'

rows=10000000
batch=10000

def update_urls_highcount():
    try:
        conn=psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASSWORD,host=DB_HOST,port=DB_PORT)
        print('Yay Connected!!!')
        cursor=conn.cursor()

        start_time=time.time()
        all_rows=gen_fakeurls(rows)

        for i in range(0,1000):
            batch_rows=all_rows[i*batch:batch*(i+1)]
            insert_query=sql.SQL('INSERT INTO url_shortener(original_url,short_code) VALUES %s')
            psycopg2.extras.execute_values(cursor,insert_query,batch_rows)
            if((i+1)%100==0):
                conn.commit() #commit every millionth step
                print(f'{batch*(i+1)} rows inserted')
            

        # for url in all_rows:
        #     insert_query='INSERT INTO url_shortener(original_url,short_code) VALUES(%s,%s)'
        #     cursor.execute(insert_query,url)

        # conn.commit()
        
        end_time=time.time() 
        print(f'Time taken to insert {len(all_rows)}: {end_time-start_time} seconds')

        cursor.close()
        conn.close()

    except Exception as e:
        print(f'An error occured:{e}')


update_urls_highcount()

