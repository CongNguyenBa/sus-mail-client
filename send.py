import sys
from os.path import dirname, abspath

current_dir = dirname(abspath(__file__))

sys.path.append(current_dir)

import socket
import utils, config

'''
Generate the email content,
without the section of addresses
'''
def mail_content(subject, body, file_path):
    boundary = utils.generate_string()

    if (len(subject) == 0):
        subject = '(no subject)'

    content = f'Subject: {subject}\r\n'
    content += f'Date: {utils.get_current_time()}\r\n'
    content += f'MIME-Version: 1.0\r\n'
    content += f'Content-Type: multipart/mixed; boundary="{boundary}"\r\n\r\n'
    content += f'--{boundary}\r\n'
    content += f'Content-Type: text/plain; charset=utf-8\r\n'
    content += f'Content-Disposition: inline\r\n'
    content += f'Content-Transfer-Encoding: 7bit\r\n\r\n'
    content += '\r\n'.join(body[i:i+100] for i in range(0, len(body), 100))
    content += f'\r\n--{boundary}\r\n'

    if (file_path != '.'):
        file_name = utils.get_file_name(file_path)
        file_content = utils.encode_attachment(file_path)
        content += f'Content-Type: application/octet-stream; name="{file_name}"\r\n'
        content += f'Content-Disposition: attachment; filename="{file_name}"\r\n'
        content += f'Content-Transfer-Encoding: base64\r\n\r\n'
        content += '\r\n'.join(file_content[i:i+100] for i in range(0, len(file_content), 100))
        content += f'\r\n--{boundary}\r\n'

    content += f'.\r\n'
    return content

'''
Send the current email to all addresses
in TO and CC
'''
def send_mail_no_bcc(from_add, to_add, cc_add, content):
    C = config.load()
    SERVER = C['HOST']
    PORT = C['SMTP']

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER, PORT))
        _ = sock.recv(2**20).decode()
    except socket.error as err:
        print(f'Unable to connect. Error {err}')
        exit()

    # START SENDING
    from_domain = utils.get_domain(from_add)
    sock.sendall(f'EHLO {from_domain}\r\n'.encode())
    _ = sock.recv(2**20).decode()

    sock.sendall(f'MAIL FROM: <{from_add}>\r\n'.encode())
    _ = sock.recv(2**20).decode()

    all_recip = to_add + cc_add

    for e in all_recip:
        sock.sendall(f'RCPT TO: <{e}>\r\n'.encode())
        _ = sock.recv(2**20).decode()

    sock.sendall(b'DATA\r\n')
    _ = sock.recv(2**20).decode()

    sock.sendall(content.encode())
    _ = sock.recv(2**20).decode()

    # Quit the session
    sock.sendall(b'QUIT\r\n')
    _ = sock.recv(2**20).decode()

    # Close the socket
    sock.close()

'''
Send current email to emails in BCC
Only one email at a time
'''
def send_bcc(from_add, bcc_add, content):
    C = config.load()
    SERVER = C['HOST']
    PORT = C['SMTP']

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER, PORT))
        _ = sock.recv(1024).decode()
    except socket.error as err:
        print(f'Unable to connect. Error {err}')
        exit()

    # START SENDING
    from_domain = utils.get_domain(from_add)
    sock.sendall(f'EHLO {from_domain}\r\n'.encode())
    _ = sock.recv(2**20).decode()
    
    sock.sendall(f'MAIL FROM: <{from_add}>\r\n'.encode())
    _ = sock.recv(2**20).decode()

    sock.sendall(f'RCPT TO: <{bcc_add}>\r\n'.encode())
    _ = sock.recv(2**20).decode()

    sock.sendall(b'DATA\r\n')
    _ = sock.recv(2**20).decode()

    sock.sendall(content.encode())
    _ = sock.recv(2**20).decode()

    sock.sendall(b'QUIT\r\n')
    _ = sock.recv(2**20).decode()

    sock.close()

'''
Interface for obtaining the addresses
'''
def mail_info():
    to_adds = []
    cc_adds = []
    bcc_adds = []
    inp = '.'
    print('Leave blank + Enter to skip\n')
    print('TO: ')
    while (inp != ''):
        inp = str(input())
        to_adds.append(inp)
        
    print('CC: ')
    inp = '.'
    while (inp != ''):
        inp = str(input())
        cc_adds.append(inp)

    print('BCC: ')
    inp = '.'
    while (inp != ''):
        inp = str(input())
        bcc_adds.append(inp)
    return to_adds, cc_adds, bcc_adds

'''
Interface for email composition
for Subject and Content
'''
def compose():
    print('Subject: ')
    subject = str(input())

    print('\nContent: (Enter . to end)')
    content = ''
    print()
    inp = ''
    while (True):
        inp = str(input())
        if (inp == '.'):
            break
        content += inp
        content += '\r\n'
    
    attMode = True
    while (attMode):
        att = str(input('\nAttachment: (Enter . to skip)\n'))
        if (att == '.'):
            attMode = False
        if (utils.check_attachment(att) == False):
            att = ''
            print('Invalid attachment. Either it is larger than 3MB or it does not exist.\n')
        else: attMode = False    
    return subject, content, att

'''
Email sender, handles the overall process
of sending email
'''
def send_main():
    C = config.load()
    from_name = C['NAME']
    from_add = C['USERNAME']
    to_add, cc_add, bcc_add = mail_info()

    subject, body, file_path = compose()

    if (len(to_add) > 0 or len(cc_add) > 0):
        content = f'From: {from_name} <{from_add}>\r\n'
        if (len(to_add) > 0):
            content += f'To: {utils.format_mail_list(to_add)}\r\n'
        if (len(cc_add) > 0):
            content += f'CC: {utils.format_mail_list(cc_add)}\r\n'
        content += mail_content(subject, body, file_path)

        send_mail_no_bcc(from_add, to_add, cc_add, content)
    
    for e in bcc_add:
        content = f'From: {from_name} <{from_add}>\r\n'
        if (len(to_add) > 0):
            content += f'To: {utils.format_mail_list(to_add)}\r\n'
        if (len(cc_add) > 0):
            content += f'CC: {utils.format_mail_list(cc_add)}\r\n'
        content += f'BCC: <{e}>\r\n'
        content += mail_content(subject, body, file_path)

        send_bcc(from_add, e, content)



