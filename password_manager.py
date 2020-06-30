# firstly user must add his master login and password, then he can add emails and passwords to his account

# importing sqlite3 - connecting to db, receiving data, inserting data etc
import sqlite3

# importing getpass - for hiding user input
import getpass

# connection to database 
conn = sqlite3.connect('password_manager.sqlite')

# getting pointer for database
cur = conn.cursor()

# creating tables in database
cur.execute('''
    CREATE TABLE IF NOT EXISTS USER
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login VARCHAR(64) UNIQUE,
        master_password VARCHAR(64)
    )
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS STORAGE
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website VARCHAR(64),
    email VARCHAR(64),
    password VARCHAR(64),
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES USER(id)
)
''')


# checking if user want to sign-up or sign-in
while True:
    type = input('Press \'C\' to create account OR \'S\' to sign-in\n')
    if type == 'C': 
        break
    elif type == 'S': 
        break



username = input('username: ')
# getpass.getpass() - user input will be hidden
user_password = getpass.getpass()
print('Hidden password:', user_password)

# checking if user exist in database
cur.execute('''
SELECT id 
FROM USER
WHERE login like ?;
''', (username, ) )

# getting user id
# cur.execute('''
# SELECT id 
# FROM USER
# WHERE login like '?'
# ''', (username) )

row = cur.fetchone()
if row is None:
    print('User is not registered in our database')
else:
    print('User is registered in our database')

row = cur.fetchone()
if row is None:
    cur.execute('''INSERT INTO USER (login, master_password) VALUES (?, ?)''', (username, user_password ) )

# inserting data to tables




# getting user id
cur.execute('''
SELECT id 
FROM USER
WHERE login like '?'
''', (username) )





#cur.execute('''INSERT INTO STORAGE (website, email, password, user_id))

# commiting the insert
conn.commit()