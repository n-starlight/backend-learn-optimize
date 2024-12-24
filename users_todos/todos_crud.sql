INSERT INTO users(name,email)
VALUES
('Sara Lance','coolninja22@blackcanary.com'),
('Barry Allen','speedster@speedforce.com'),
('Oliver Queen','greenarrow11@balckcanary.com'),
('Mia Smoak','greenarrow33@blackcanary.com')


INSERT INTO todos(title,user_id)
VALUES
('Challenge Anti-Monitor',4),
('Avenge Red Arrow Crisis',3),
('No Arrows Mission',3),
('Train League of Heroes',1),
('Regain lost Speed Force',2),
('Make perfect Noodles Dish',4),
('Start League of Heroes',1),
('Hire for League of Heroes',1),
('Increase Speed',2)

UPDATE todos SET is_completed = TRUE WHERE user_id = 4;

SELECT id, title, is_completed, created_at
FROM todos
WHERE user_id = 4
ORDER BY created_at;

ALTER TABLE todos
ADD COLUMN due_date DATE;

--to set due_date default to created_at + 15 days ,so for setting default based on another
--column trigger function is needed.

--function to update a  col's values based on another col's values
CREATE OR REPLACE FUNCTION set_def_duedate()
RETURNS TRIGGER AS $$   #here returns a trigger function(trigger function is defined here)
BEGIN
    -- Only set due_date if it's not already provided
    IF NEW.due_date IS NULL THEN
        NEW.due_date := NEW.created_at + INTERVAL '15 days';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;



CREATE TRIGGER trigger_default_duedate  #creates a trigger function like declaring a function
BEFORE INSERT 
ON todos             
FOR EACH ROW
EXECUTE FUNCTION set_def_duedate();   #this func is executed for every row before insert

UPDATE todos
SET due_date=
CASE
WHEN users.id=1 THEN '2024-11-01'
WHEN users.id=2 THEN '2024-10-25'
WHEN users.id=3 THEN '2024-11-05'
WHEN users.id=4 THEN '2024-11-10'
ELSE due_date
END
FROM users     # as id is referenced from users table
WHERE todos.user_id=users.id;

SELECT todos.id,users.name,todos.title,todos.due_date
FROM todos
JOIN users ON todos.user_id=users.id  
ORDER BY id ASC;

SELECT todos.id,users.name,todos.title,todos.is_completed,todos.due_date FROM todos
JOIN users ON todos.user_id=users.id
WHERE due_date< CURRENT_DATE AND is_completed=false
ORDER BY due_date

SELECT subquery.todoos_count,users.name
FROM (
SELECT user_id,COUNT(todos.title) as todoos_count
FROM todos
GROUP BY
user_id
) AS subquery   # the subquery here is a aggregated table itself
JOIN users on subquery.user_id=users.id ;

ALTER TABLE todos
ADD COLUMN description VARCHAR(550);


UPDATE todos
SET description=
CASE
WHEN todos.id=1 THEN 'Find ways to defet anti-monitor'
WHEN todos.id=3 THEN 'Use no Arrows'
WHEN todos.id=4 THEN 'Teach new fight variations'
WHEN todos.id=9 THEN 'Learn 3rd new basic variation'
ELSE description
END

ALTER TABLE todos
DROP CONSTRAINT IF EXISTS todos_user_id_fkey;

ALTER TABLE todos
ADD CONSTRAINT todos_user_id_fkey
FOREIGN KEY(user_id) REFERENCES users(id)
ON DELETE CASCADE;

DELETE FROM users
WHERE id=5;

SELECT u.name,t.title,latest.latest_created_at
FROM(
SELECT user_id,MAX(created_at) AS latest_created_at
FROM todos 
GROUP BY user_id
) AS latest
RIGHT JOIN users u ON latest.user_id=u.id
JOIN todos t ON latest.user_id=t.user_id AND latest.latest_created_at = t.created_at;

SELECT
users.id,
users.name,
users.email,
counts_table.completed_todos,
counts_table.uncompleted_todos,
counts_table.total_todos
FROM (
SELECT
user_id,
COUNT(CASE WHEN todos.is_completed = True AND todos.due_date<CURRENT_DATE THEN 1 END) AS completed_todos,
COUNT(CASE WHEN todos.is_completed = False AND todos.due_date<CURRENT_DATE THEN 1 END) AS uncompleted_todos,
COUNT(title) as total_todos
FROM todos
GROUP BY todos.user_id
) AS counts_table
JOIN
users ON counts_table.user_id=users.id;

ALTER TABLE todos
RENAME COLUMN is_completed TO status ;

ALTER TABLE todos
ALTER status TYPE VARCHAR(15) USING status::VARCHAR(15) ;

UPDATE todos
SET status=
CASE
WHEN todos.status='false' AND due_date<CURRENT_DATE THEN 'PENDING'
WHEN todos.status='true' AND due_date<CURRENT_DATE THEN 'COMPLETED'
WHEN todos.status='false' AND due_date>CURRENT_DATE THEN 'IN_PROGRESS'
ELSE status
END

CREATE INDEX CONCURRENTLY idx_todos_user_id ON todos(user_id);

--user_id indexes size=822 MB

--TABLE SIZE 12 GB

SELECT users.id, users.name, users.email FROM users
WHERE users.id IN(
SELECT user_id
FROM todos
WHERE created_at>=CURRENT_DATE- INTERVAL '1 month'
GROUP BY user_id
HAVING SUM(CASE WHEN is_completed=true THEN 1 ELSE 0 END ) = 0
LIMIT 1000
)