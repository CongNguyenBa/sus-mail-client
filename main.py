import start, send, retr, folder
import os

'''
Commented at 10:23 AM, Sat, Dec 16 2023
'''

'''
------ MAIN FUNCTION ------
Operates the whole program
'''
def main():
    folder.init_folder()
    while True:
        os.system('cls')
        key = start.start_main()
        if (key == 1):
            os.system('cls')
            send.send_main()
        elif (key == 2):
            os.system('cls')
            retr.retr_main()
        elif (key == 3):
            exit()
        else: continue

if __name__ == '__main__':
    main()