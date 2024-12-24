
import psycopg2
import getpass
import time
from psycopg2 import sql
import psycopg2.extras
import random
import string

from gen_fakeurls import gen_fakeurls,gen_unique_codes

DB_NAME='URL_SHORTENER'
DB_USER='postgres'
DB_PASSWORD=getpass.getpass('Enter you Password: ')
DB_HOST='localhost'
DB_PORT='5432'

# rows=10000000
rows=100_000 # for 2nd trial
batch=10_000

rows1=100

base_domains=['https://scikit-image.org/docs/stable/api/skimage.feature.html',
                 'https://scikit-image.org/docs/stable/api/skimage.color.html','https://github.com/','https://medium.com/@']

def update_urls_highcount():
    conn=psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASSWORD,host=DB_HOST,port=DB_PORT)
    print('Yay Connected!!!')
    if not conn:
        return
    try:
        cursor=conn.cursor()
        


        start_time=time.time()

        fetch_query = "SELECT short_code FROM url_shortener;"
        cursor.execute(fetch_query)
        fetch_rows=cursor.fetchall()
        existing_short_codes=[row[0] for row in fetch_rows]
        success_count=0

        end_time=time.time() 
        print(f'time to fetch existing short_codes: {end_time-start_time}')
        
        start_time=time.time()

        all_urls=[]

        while success_count<rows :     # for 2nd time
            new_code=gen_unique_codes(5)
            if new_code not in existing_short_codes:
                first_part=random.choice(base_domains)
                last_part=f'?param{gen_unique_codes(13)}' if first_part in base_domains[:2] else f'{gen_unique_codes(7)}'
                long_url=f'{first_part}{last_part}'
                all_urls.append((long_url,new_code))
                success_count+=1

        # all_rows=gen_fakeurls(rows)


        end_time=time.time() 
        print(f'time to generate urls and short codes: {end_time-start_time}')

        loops=int(rows/batch)  # inserting numbers so that rows/batch is fully divisible

        start_time=time.time()

        for i in range(0,loops):
            # batch_rows=all_rows[i*batch:batch*(i+1)]
            batch_rows=all_urls[i*batch:batch*(i+1)]
            insert_query=sql.SQL('INSERT INTO url_shortener(original_url,short_code) VALUES %s')
            psycopg2.extras.execute_values(cursor,insert_query,batch_rows)
            # if((i+1)%100==0):
            #     conn.commit() #commit every millionth step(1st trial for 10 million)
            #     print(f'{batch*(i+1)} rows inserted')
            conn.commit()
            print(f'{batch*(i+1)} rows inserted')
            

        
        
        end_time=time.time() 
        # print(f'Time taken to insert {len(all_rows)}: {end_time-start_time} seconds')
        print(f'Time taken to insert {len(all_urls)}: {end_time-start_time} seconds')

        cursor.close()
        conn.close()

    except Exception as e:
        print(f'An error occured:{e}')
        conn.rollback()
        cursor.close()
        conn.close()


update_urls_highcount()

