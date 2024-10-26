import psycopg2
import getpass
from psycopg2 import sql
import time
import psycopg2.extras

DB_NAME='TODOS'
DB_USER='postgres'
DB_PASSWORD=getpass.getpass('Enter you Password: ')
DB_HOST='localhost'
DB_PORT='5432'

def search_for_input(search_input):
    try:
        conn=psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASSWORD,host=DB_HOST,port=DB_PORT)
        print('Yay Connected!!!')
        cursor=conn.cursor()

        # start_time=time.time()
        # index_query="""
        # CREATE INDEX IF NOT EXISTS todos_fulltext_idx ON todos USING GIN (to_tsvector('english', title || ' ' || description));
        # """
        # cursor.execute(index_query)

        # end_time=time.time()
        # print(f'Time taken to create indexes on full text in table: {end_time-start_time} seconds')

        start_time=time.time()

        search_query="""
        SELECT title
        FROM todos
        WHERE to_tsvector('english',title) @@ to_tsquery('english', %s)
        """
        search_term=' & '.join(search_input.split()) if " " in search_input else search_input

        cursor.execute(search_query,(search_term,))

        fetch_results=cursor.fetchall()

        for r in fetch_results:
            print('title: ',r[0])
            print('----')

        end_time=time.time() 
        print(f'Time taken to search in approx 100 million todos: {end_time-start_time} seconds')

        cursor.close()
        conn.close()

        

    except Exception as e:
        print(f'An error occured:{e}')

user_input=input('Enter anything to search for: ')
search_for_input(user_input)