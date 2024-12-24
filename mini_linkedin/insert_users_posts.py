# import random
# import string
# import getpass
# from psycopg2 import sql
# import time
# import psycopg2.extras
# from gen_data import gen_fake_user

# DB_NAME='schema_stable'
# DB_USER='postgres'
# DB_PASSWORD=getpass.getpass('Enter you Password: ')
# DB_HOST='localhost'
# DB_PORT='5432'

# users=10_000
# posts=100
# likes=10_000


# def db_connection():
#     try:
#         conn=psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASSWORD,host=DB_HOST,port=DB_PORT)
#         print('Yay Connected!!!')
#         return conn
#     except Exception as e:
#         print(f"Error connecting to database: {e}")
#         return None



# def insert_users(cursor,conn):
#     start_time=time.time()
#     batch=1000
#     loops=int(users/batch)

#     for i in range(0,loops):
#         batch_users=[gen_fake_user() for _ in range(batch)]
#         insert_query="INSERT INTO users (name,email,created_at) VALUES %s"
#         psycopg2.extras.execute_values(cursor,insert_query,batch_users)
#         conn.commit()
#         print(f'{batch*(i+1)} inserted out of {users}')
        
#     end_time=time.time() 
#     print(f'Time taken to insert users {end_time-start_time} seconds')

# def insert_posts(cursor,conn):
#     start_time=time.time()
#     batch=100
#     loops=int(posts/batch)
#     for i in range(0,loops):
#         batch_posts=[gen_fake_todo(random.randint(1,users)) for _ in range(batch)]
#         insert_query='INSERT INTO posts(title,user_id,status,created_at,due_date,description,is_completed) VALUES %s'
#         psycopg2.extras.execute_values(cursor,insert_query,batch_todos)
#     conn.commit()
#     end_time=time.time()
#     print(f'Time taken to insert posts {end_time-start_time} seconds') 

# def insert_likes(cursor,conn):
#     start_time=time.time()
#     batch=100
#     loops=int(posts/batch)
#     for i in range(0,loops):
#         batch_posts=[gen_fake_todo(random.randint(1,users)) for _ in range(batch)]
#         insert_query='INSERT INTO posts(title,user_id,status,created_at,due_date,description,is_completed) VALUES %s'
#         psycopg2.extras.execute_values(cursor,insert_query,batch_todos)
#     conn.commit()
#     end_time=time.time() 

# def main():
#     conn=db_connection()
#     if not conn:
#         return
#     try:
#         cursor=conn.cursor()

#         user_input=input('Do you want to update or insert? ').lower()
#         if(user_input=='update'):
#             migrate_schema(cursor,conn)
#             print('Updation done successfully!')
#         elif(user_input=='insert'):
#             insert_schema(cursor,conn)
#         else:
#             print("Invalid input. Please choose 'Update' or 'Insert' ") 

#     except Exception as e:
#         print(f"Error during database operation: {e}")
#         conn.rollback()

#     finally:
#         cursor.close()
#         conn.close()




# if __name__=="__main__":
#     main()