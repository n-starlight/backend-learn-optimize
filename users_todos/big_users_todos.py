
import psycopg2
import getpass
from psycopg2 import sql
import time
import random
import psycopg2.extras

from gen_fake_users import gen_fake_user,gen_fake_todo,set_priority

DB_NAME='TODOS'
DB_USER='postgres'
DB_PASSWORD=getpass.getpass('Enter you Password: ')
DB_HOST='localhost'
DB_PORT='5432'

users=10_000_000
todos=100_000_000
batch=10_000



def db_connection():
    try:
        conn=psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASSWORD,host=DB_HOST,port=DB_PORT)
        print('Yay Connected!!!')
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None



def main():
    conn=db_connection()
    if not conn:
        return
    try:
        cursor=conn.cursor()

        # start_time=time.time()


        # print(f'inserting users in batches of {batch}') 
        # is_present='SELECT COUNT(*) FROM users'
        # cursor.execute(is_present)
        # users_present = cursor.fetchone()[0] 
        # if users_present<20:

        # fetchquery='SELECT COUNT(*) FROM todos'
        # cursor.execute(fetchquery)
        # todos_count=cursor.fetchone()[0]
        # print(todos_count)

        # end_time=time.time()

        # print(f'Time taken to fetch count of todos {end_time-start_time} seconds')

        start_time=time.time()


        # users_loops=int(users/batch)
        # todos_loops=int(todos/batch)
        # for i in range(0,users_loops):
        #     batch_users=[gen_fake_user() for _ in range(batch)]
        #     insert_query=sql.SQL('INSERT INTO users(name,email,created_at) VALUES %s')
        #     psycopg2.extras.execute_values(cursor,insert_query,batch_users)
        #     if((i+1)%int(users_loops/10)==0):
        #             conn.commit() 
        #             print(f'{batch*(i+1)} users inserted out of {users}')
        # else:
        #     print('Users already added !')
            
        

        # print(f'inserting todos in batches of {batch}') 
        # for i in range(0,todos_loops):
        #     batch_todos=[gen_fake_todo(random.randint(1,users)) for _ in range(batch)]
        #     insert_query=sql.SQL('INSERT INTO todos(title,user_id,status,created_at,due_date,description,is_completed) VALUES %s')
        #     psycopg2.extras.execute_values(cursor,insert_query,batch_todos)
        #     if((i+1)%int(todos_loops/10)==0):
        #         conn.commit() 
        #         print(f'{batch*(i+1)} todos inserted out of {todos}')
        
        #inserting too much todos for a user
        # print(f'inserting 10M todos for a user') 
        # for i in range(0,10_000):
        #     batch_todos=[gen_fake_todo(5) for _ in range(batch)]
        #     insert_query=sql.SQL('INSERT INTO todos(title,user_id,status,created_at,due_date,description,is_completed) VALUES %s')
        #     psycopg2.extras.execute_values(cursor,insert_query,batch_todos)
        #     if((i+1)%10==0):
        #         conn.commit() 
        #         print(f'{batch*(i+1)} todos inserted out of {todos}')

        for skip in range(0,1_000_000,batch):
            cursor.execute(f"""
                SELECT id,due_date,created_at,is_completed
                FROM todos
                ORDER BY id
                LIMIT {batch} OFFSET {skip}; 
            """)
        
            batch_todos=cursor.fetchall()
            updates = [(set_priority(due_date=todo[1],created_at=todo[2],is_completed=todo[3]), todo[0]) for todo in batch_todos]

            update_query="""
            UPDATE todos
            SET priority=updates.priority
            FROM (VALUES %s) AS updates (priority,id)
            WHERE todos.id=updates.id
            """
            psycopg2.extras.execute_values(cursor,update_query,updates)
            conn.commit()
            print(f'Updated {skip + batch} of 1_000_000 rows')

            
        
        end_time=time.time() 
        # print(f'Time taken to insert all users and todos: {end_time-start_time} seconds')
        print(f'Time taken to update todos priority (1 million) {end_time-start_time} seconds')


        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error during database operation: {e}")
        conn.rollback()
        cursor.close()
        conn.close()



if __name__=="__main__":
    main()