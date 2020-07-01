# firstly user must add his master login and password, then he can add emails and passwords to his account

# importing sqlite3 - connecting to db, receiving data, inserting data etc
import sqlite3

# importing getpass - for hiding user input
from getpass import getpass

# for hashing passwords
import bcrypt

# tables
import termtables as tt

# creating User Class
class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username


#functions declaration     
def hash_password(password):
    hashed_password = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt())
    return hashed_password


def password_validation(user_password, hashed_password_from_db):
    return bcrypt.checkpw(user_password.encode(), hashed_pass_from_db)


def addData():
    website_url = input('Website url: ')
    website_login = input('Login: ')
    website_password = getpass('Password: ')

    cur.execute('INSERT INTO STORAGE (website, email, password, user_id) VALUES (?, ?, ?, ?)', (website_url, website_login, website_password, current_user.id) )
    conn.commit()
    # print(website_url, website_login, website_password)


def showData():
    # print('Show data function')
    # print('User id: ', current_user.id)
    try:
        cur.execute('SELECT website, email, password FROM STORAGE WHERE user_id like ?', (current_user.id, ) )
        password_data_array = cur.fetchall()

        if password_data_array is None:
            print('No data to display')
        else:
            formatted_table_with_data = tt.to_string(
                password_data_array,
                header = ['website', 'email', 'password'],
                style = tt.styles.ascii_thin_double
            )
            print(formatted_table_with_data)
    except:
        print('No data to display')

def showData_from_URL(website_url):
    try:
        cur.execute('SELECT website, email, password FROM STORAGE WHERE user_id like ? AND website like ?', (current_user.id, website_url) )
        password_data_array = cur.fetchall()

        if password_data_array is None:
            print('No data to display')
        else:
            formatted_table_with_data = tt.to_string(
                password_data_array,
                header = ['website', 'email', 'password'],
                style = tt.styles.ascii_thin_double
            )
            print(formatted_table_with_data)
    except:
        print('No data to display')


def modifyData():
    print('Modyfying data')
    website_url = input('From which website: ')
    website_email = input('Email: ')
    website_password = getpass('New password: ')

    try:
        print('\nUpdating...')
        cur.execute('UPDATE STORAGE SET password = ? WHERE website like ? AND email like ? AND user_id like ?', (website_password, website_url, website_email, current_user.id))
        conn.commit()
        print('Updated')
    except:
        print('Couldn\'t Update')


def removeData():
    print('Removing Data')
    website_url = input('From which website: ')
    website_email = input('Email: ')

    try:
        print('\nRemoving...')
        cur.execute('DELETE FROM STORAGE where website like ? AND email like ?', (website_url, website_email))
        conn.commit()
        print('Removed')
    except:
        print('Could not remove')



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
        master_password BINARY(60)
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

# create current_user var
current_user = None

# checking if user want to sign-up or sign-in
while True:
    type = input('Press \'C\' to create account OR \'S\' to sign-in\n').upper()
    if type == 'C' or type == 'S':
        break


if type == 'C':
    while True:  
        username = input('\nusername: ')
        # getpass.getpass() - user input will be hidden
        user_password = getpass('Password: ')
        # checking if username exists in database
        cur.execute('SELECT id FROM USER WHERE login like ?', (username, ) )

        if cur.fetchone() is None:
            hashed_password = hash_password(user_password)
            cur.execute('INSERT INTO USER (login, master_password) VALUES (?, ?)', (username, hashed_password, ) )
            conn.commit()
            # print('User created')
            
            cur.execute('SELECT id, login FROM USER where login like ? ', (username, ) )
            row = cur.fetchone()

            # adding data to current_user object
            current_user = User(row[0], row[1])


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
            print('Username ', username,'doesn\'t exist\n')
            continue

        user_password = getpass('Password: ')
        
        # checking if username and password are correct
        hashed_pass_from_db = row[0]
        
        if password_validation(user_password, hashed_pass_from_db):
            cur.execute('SELECT id, login FROM USER where login like ?', (username, ) )
            row = cur.fetchone()

            # adding data to current_user object
            current_user = User(row[0], row[1])
        else:
            print('The data you have entered are incorrect')
            continue
        
        print('Congratulations you are logged in!')
        break

        
while True:
    print('\nWhat you want to do?')
    key_pressed = input('Press \'A\' for adding data, \'S\' for showing data,\'R\' to remove data or \'M\' to modify, press enter to quit\n').upper()
    
    if key_pressed != 'A' or key_pressed != 'S':
        
        if key_pressed == '':
            print('Goodbye', current_user.username)
            break
        elif key_pressed == 'A':
            addData()
        elif key_pressed == 'S':
            website_url = input("Enter website name or press enter to show all data: ")
            if website_url == '':
                showData()
            else:
                showData_from_URL(website_url)
        elif key_pressed == 'R':
            removeData()
        elif key_pressed == 'M':
            modifyData()
        else:
            print('You pressed wrong key. Try Again.\n')
            
