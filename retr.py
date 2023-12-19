import socket, os, base64, threading

import config, filter, folder, utils, history

'''
----- RETRIEVING EMAILS -----
'''

'''
Obtain emails from the server
'''
def get_mails():
    C = config.load()
    usr = C['USERNAME']
    pwd = C['PASSWORD']
    host = C['HOST']
    port = C['POP3']

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        
    except socket.error as err:
        print(f'Can not connect. Error here: {err}')
        exit()
    res = sock.recv(2**20).decode()

    sock.sendall(f'USER {usr}\r\n'.encode())
    res = sock.recv(2**20).decode()
    
    sock.sendall(f'PASS {pwd}\r\n'.encode())
    res = sock.recv(2**20).decode()

    sock.sendall('STAT\r\n'.encode())
    res = sock.recv(2**20).decode()
    
    sock.sendall('LIST\r\n'.encode())
    res = sock.recv(2**20).decode()

    sock.sendall('UIDL\r\n'.encode())
    res = sock.recv(2**20).decode()
    
    lines = res.splitlines()[1:-1]
    for l in lines:
        idx, file_name = l.split(' ')
        sock.sendall(f'RETR {idx}\r\n'.encode())
        msg = sock.recv(2**20).decode()
        
        save_mail(file_name, msg)

    sock.sendall('QUIT\r\n'.encode())
    res = sock.recv(2**20).decode()

'''
Call the email filtering function
'''
def filter_mail(msg):
    F = filter.Filter()
    return F.filter(msg)

'''
Save the email to local folder
'''
def save_mail(name, msg):
    subfolder = filter_mail(msg)
    subject = utils.get_subject(msg)
    path = folder.get_mailbox_dir()
    path = os.path.join(path, subfolder)
    new_file_name = f'{subject}_{name}'

    file_path = os.path.join(path, new_file_name)
    with open(file_path, 'w') as f:
        f.write(msg)
        f.close()
# ----------------------------------------------------------
# FRONT-END

'''
Interface, ask user whether to save the current attachment.
'''
def file_dialog(name):
    print('\n\033[0;31;40m')
    choice = str(input(f'Attachment: {name}. \nWould you like to save? (y for Yes)\033[0;0m\n'))
    if (choice == 'y'):
        return True
    else: return False

'''
Download attachment to local folder
'''    
def download_file(output_file, input_base64):
    dest_folder = folder.get_attachment_dir()
    binary_data = base64.b64decode(input_base64)
    output_path = os.path.join(dest_folder, output_file)

    with open(output_path, 'wb') as f:
        f.write(binary_data)

'''
Interface to read an email,
which includes all content and attachments-related dialogs
'''
def view_mail(path):
    os.system('cls')
    with open(path, 'r') as F:
        msg = F.read()
    

    history.write(utils.get_file_name(path))

    os.system('cls')
    s = utils.get_subject(msg)
    fr = utils.get_from(msg)
    to = utils.get_to(msg)
    cc = utils.get_cc(msg)
    bcc = utils.get_bcc(msg)
    content = utils.get_inline(msg)

    print('\033[0;33;40m')
    print(f'FROM: {fr}')
    print(f'TO: {to}')
    print(f'CC: {cc}')
    print(f'BCC: {bcc}')
    print('\033[0;0m')
    print()
    print('----------------------------')
    print('\033[1;37;40m')
    print(f'Subject: {s}')
    print('\033[0;0m')

    print('----------------------------')
    print(content)
    print('----------------------------')
    
    attachments = utils.get_attachment(msg)

    for item in attachments:
        name = item[0][0]
        dlChoice = file_dialog(name)
        if (dlChoice == True): download_file(item[0][0], item[1])
        
    input()
    show_mailbox_subfolders_and_choose()

'''
Interface showing the subfolders of the mailbox,
asking the user the choose the desired folder
'''
def show_mailbox_subfolders_and_choose():
    os.system('cls')
    directory = folder.get_mailbox_dir()
    subfolders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    print('----------------------------')

    if not subfolders:
        print("No subfolders found in this directory.")
        exit()

    print("Folders:\n")
    for i, F in enumerate(subfolders):
        print(f"{i + 1}: {F}")
    print('----------------------------')

    while True:
        try:
            choice = int(input("Enter the index of the subfolder you want to choose: "))
            if 0 <= choice < len(subfolders):
                chosen_folder = os.path.join(directory, subfolders[choice - 1])
                show_files_in_folder(chosen_folder)
            else:
                print("Invalid index. Please enter a valid index.")
        except ValueError:
            print("Invalid input. Please enter a number.")

'''
Show emails in the current folder
asking user which email to read
'''
def show_files_in_folder(folder_path):
    os.system('cls')
    H = history.load()
    files = os.listdir(folder_path)
    print('----------------------------')
    if not files:
        print("No messages found in the folder. Enter to continue.")
        input()
        show_mailbox_subfolders_and_choose()

    
    print("Mails in this folder:")
    print('----------------------------')
    for i, file in enumerate(files):
        if file not in H:
            status = '[UNREAD]'
        else: status = ''

        print('\033[0;36;40m')
        print(f"{i + 1}. {file}      \033[1;31;43m{status}\033[0;0m")
    print('----------------------------')
    
    while True:
        try:
            choice = int(input("Enter the index of the mail you want to choose (or 0 to exit): "))
            if choice == 0:
                exit()
            elif 0 < choice <= len(files):
                dest_mail = os.path.join(folder_path, files[choice - 1])
                view_mail(dest_mail)
            else:
                print("Invalid index. Please enter a valid index or 0 to exit.")
        except ValueError:
            print("Invalid input. Please enter a number.")

'''
Automatically sync emails from the server in background
'''
def sync_mails(interval):
    while True:
        get_mails()
        threading.Event().wait(interval)

'''
Main function for operating the mail retrieving process
and the mailbox
'''
def retr_main():
    C = config.load()
    itv = C['SYNC_INTERVAL']
    thr = threading.Thread(target=sync_mails, args=(itv,))

    thr.daemon = True
    thr.start()
    show_mailbox_subfolders_and_choose()