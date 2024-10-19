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




start_time = time.time()

query='''WITH rand_short_codes as(
    SELECT short_code
	FROM url_shortener
	ORDER BY random()
	LIMIT 4
)

SELECT original_url,short_code
FROM url_shortener
WHERE short_code in (SELECT short_code FROM rand_short_codes);
'''

total_runs=1000000


for _ in range(total_runs):
    cursor.execute(query)
    

end_time = time.time()


print(f"Total time taken for {len(total_runs)} : {end_time - start_time:.2f} seconds")


cursor.close()
conn.close()