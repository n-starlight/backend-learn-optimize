import random
import string
import datetime

 

def gen_fake_user():
    first_name=''.join(random.choices(string.ascii_uppercase,k=1)) +''.join(random.choices(string.ascii_lowercase,k=7))
    last_name=''.join(random.choices(string.ascii_uppercase,k=1)) +''.join(random.choices(string.ascii_lowercase,k=7))
    name=f'{first_name}{last_name}'
    email=f'{last_name.lower()}@{first_name[:2]}{"".join(random.choices(string.digits, k=3))}'
    created_at=datetime.datetime.now()+datetime.timedelta(days=random.randint(-30,-15))
    return (name,email,created_at)

def gen_fake_todo(user_id):
    title=''.join(random.choices(string.ascii_uppercase,k=16))
    created_at=datetime.datetime.now()+datetime.timedelta(days=random.randint(-15,10))
    due_date = created_at.date()+datetime.timedelta(days=random.randint(1,25))
    is_completed=random.choice((True,False)) if due_date<datetime.date.today() else False
    description=''.join(random.choices(string.ascii_uppercase,k=25))

    status='IN_PROGRESS'
    
    if is_completed==False and due_date<datetime.date.today():
        status='PENDING'
    elif is_completed==True and due_date<datetime.date.today():
        status='COMPLETED'
    elif is_completed==False and due_date>=datetime.date.today():
        status='IN_PROGRESS'

    return (title,user_id,status,created_at,due_date,description,is_completed)

def set_priority(due_date,created_at,is_completed):
    if due_date<datetime.datetime.now().date() and is_completed==False :
        priority=2
    elif (due_date - created_at.date()).days in [0,6]:
        priority=2
    elif (due_date - created_at.date()).days in [6,16]:
        priority=1
    else:
        priority=0

    return priority