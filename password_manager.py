# firstly user must add his master login and password, then he can add emails and passwords to his account

# importing sqlite3 - connecting to db, receiving data, inserting data etc
import sqlite3

# importing getpass - for hiding user input
from getpass import getpass

# for hashing passwords
import bcrypt

# tables
import termtables as tt
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

row_with_id_number = None

if type == 'C':
    while True:  
        username = input('username: ')
        # getpass.getpass() - user input will be hidden
        user_password = getpass('Password: ')
        # checking if username exists in database
        cur.execute('SELECT id FROM USER WHERE login like ?', (username, ) )

        if cur.fetchone() is None:
            hashed_password = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt())
            cur.execute('INSERT INTO USER (login, master_password) VALUES (?, ?)', (username, hashed_password, ) )
            conn.commit()
            print('User created')
            
            cur.execute('SELECT id FROM USER where login like ? ', (username, ) )
            row_with_id_number = cur.fetchone()
            print('Congratulations you are logged in!')
            break
        else:
            print('Account with this username exists. ')
else:
    while True:
        username = input('username: ')
        # getpass.getpass() - user input will be hidden
        cur.execute('SELECT master_password FROM USER where login like ?', (username,) )
        row = cur.fetchone()

        if row is None:
            print('Username ', username,'doesnt exist\n')
            continue

        user_password = getpass('Password: ')
        
        # checking if username and password are correct
        hashed_password = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt())
        

        hashed_pass_from_db = row[0]
        
        validation = bcrypt.checkpw(user_password.encode(), hashed_pass_from_db)

        if validation:
            cur.execute('SELECT id FROM USER where login like ?', (username, ) )
            row_with_id_number = cur.fetchone()

        if row_with_id_number is None:
            print('The data you have entered are incorrect')
        else:
            print('Congratulations you are logged in!')
            break

current_user_id = row_with_id_number[0]
# print('User id: ', user_id)

def showData():
    cur.execute('SELECT website, email, password FROM STORAGE WHERE user_id like ?', (current_user_id, ) )
    password_data_array = cur.fetchall()

    formatted_table_with_data = tt.to_string(
        password_data_array,
        header = ['website', 'email', 'password'],
        style = tt.styles.ascii_thin_double
    )
    print(formatted_table_with_data)
        
showData()