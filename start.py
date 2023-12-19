import config 
import os, json

'''
----- START INTERFACE -----
Commented at 10:10, Dec 16 2023 
'''

# Welcome Interface
def info():
    print('\033[0;33;40m')
    print('-------------------------------------------------')
    print('Welcome to SUS Mail Client.')
    print()
    print()
    print('SUS stands for Simple-Unencrypted-Single Sign-on.')
    print('-------------------------------------------------')
    print('\033[0;0m')

# Login interface
def login_i():
    print('Let\'s sign in!')
    print('Full name: ')
    name = str(input())
    print('Email: ')
    email = str(input())
    print('Password: ')
    pwd = str(input())
    return name, email, pwd

# Login process
def login():
    C = config.load()
    usr = C['USERNAME']
    pwd = C['PASSWORD']

    if (len(usr) == 0):
        name, usr, pwd = login_i()
        with open('config.json', 'r') as f:
            data = json.load(f)
        data['NAME'] = name
        data['USERNAME'] = usr
        data['PASSWORD'] = pwd

        with open('config.json', 'w') as f:
            json.dump(data, f, indent=4)
    else:
        print(f'You are logged in as {usr}.')
    
# Menu interface, return the choice
def menu():
    print('\033[0;34;40m')
    print('\n--------- MENU ---------')
    print('1. Compose Email')
    print('2. Open Inbox')
    print('3. Exit')
    print('\n________________________')
    print('\033[0;0m')
    choice = int(input('\nYour choice: '))
    return choice

# Welcome and Menu screen handler
def start_main():
    os.system('cls') # Clears screen
    info()
    login()
    key = menu()
    return key