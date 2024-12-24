import random
import string
import getpass
from psycopg2 import sql
import time
import psycopg2.extras

DB_NAME='schema_stable'
DB_USER='postgres'
DB_PASSWORD=getpass.getpass('Enter you Password: ')
DB_HOST='localhost'
DB_PORT='5432'

users=100_000_000
batch=10_000

def db_connection():
    try:
        conn=psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASSWORD,host=DB_HOST,port=DB_PORT)
        print('Yay Connected!!!')
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def gen_measures():
    name=''.join(random.choices(string.ascii_uppercase,k=1)) + ''.join(random.choices(string.ascii_lowercase,k=8))
    feet=random.choice([random.randint(0,9),random.randint(10,100)])
    inches=random.randint(1,12) 
    return (name,feet,inches)

def migrate_schema(cursor,conn):

    start_time = time.time()
    
    #1: Add the new column
    cursor.execute("ALTER TABLE measurements ADD COLUMN total_inches INT")
    
    #2: Populate total_inches based on feet and inches
    
    for skip in range(0,users,batch):
           update_query="""
           UPDATE measurements
           SET total_inches=(feet*12) + inches
           WHERE id BETWEEN %s AND %s
           """
           cursor.execute(update_query,(skip+1,skip+batch))
           conn.commit()
           print(f'Updated {skip + batch} rows')

    end_time=time.time()
    print(f'Time taken for updation {end_time-start_time}')
    
    #3: Drop old columns
    start_time = time.time()
    cursor.execute("ALTER TABLE measurements DROP COLUMN feet, DROP COLUMN inches")
    end_time=time.time()
    print(f'Time taken for drop {end_time-start_time}')

def insert_schema(cursor,conn):
    start_time=time.time()

    loops=int(users/batch)

    for i in range(0,loops):
        batch_users=[gen_measures() for _ in range(batch)]
        insert_query="INSERT INTO measurements (name,feet,inches) VALUES %s"
        psycopg2.extras.execute_values(cursor,insert_query,batch_users)
        if((i+1)%1000==0):
            conn.commit()
            print(f'{batch*(i+1)} inserted out of {users}')
        
    end_time=time.time() 
    print(f'Time taken {end_time-start_time} seconds')

def main():
    conn=db_connection()
    if not conn:
        return
    try:
        cursor=conn.cursor()

        user_input=input('Do you want to update or insert? ').lower()
        if(user_input=='update'):
            migrate_schema(cursor,conn)
            print('Updation done successfully!')
        elif(user_input=='insert'):
            insert_schema(cursor,conn)
        else:
            print("Invalid input. Please choose 'Update' or 'Insert' ") 

    except Exception as e:
        print(f"Error during database operation: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()




if __name__=="__main__":
    main()