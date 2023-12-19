from datetime import datetime
import tzlocal

# Boundary string
import secrets, string
import base64, os, re


def encode_attachment(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
        encoded_content = base64.b64encode(file_content).decode('utf-8')
    return encoded_content

def get_file_name(file_path):
    return os.path.basename(file_path)

def generate_string():
    L = 20
    res = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(L))
    return str(res)

def format_mail_list(address_list):
    return ', '.join([f'<{address}>' for address in address_list])

def get_current_time():
    local_tz = tzlocal.get_localzone()
    current_date_time = datetime.now(local_tz)
    formatted_current_date_time = current_date_time.strftime('%a, %d %b %Y %H:%M:%S %z')
    return formatted_current_date_time

def get_domain(address):
    try:
        _, domain = address.split('@')
        return domain
    except ValueError:
        raise ValueError('Invalid email address format')
    
def debug_to_file(debug_string, file_name='debug_output.txt'):
    try:
        with open(file_name, 'w') as file:
            file.write(debug_string)
        print(f"Debug information written to '{file_name}' successfully.")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

'''
Check if the attachment is valid
It checks both the availability and size validity of the file
'''
def check_attachment(file_path):
    if (os.path.exists(file_path)):
        file_size = os.path.getsize(file_path)
        if file_size <= (3 * 1024 * 1024):
            return True
        else: return False
    else: return False

'''
-----------------------------------------------------
        EMAIL RETRIEVING FUNCTIONS
'''
'''
4 functions below work the same way
They do what their names suggest:
Get the sender address (from), recipient address (to)
CC & BCC addresses and date of the email
'''
def get_from(msg):
    l = msg.find('From: ') + len('From: ')
    r = msg.find('\n', l)
    if l != -1 and r != -1:
        return msg[l:r].strip()
    return ""

def get_to(msg):
    l = msg.find('To: ') + len('To: ')
    r = msg.find('\n', l)
    if l != -1 and r != -1:
        return msg[l:r].strip()
    return ""

def get_cc(msg):
    l = msg.find('CC: ') + len('To: ')
    r = msg.find('\n', l)
    if l != -1 and r != -1:
        return msg[l:r].strip()
    return ""

def get_bcc(msg):
    l = msg.find('CC: ') + len('To: ')
    r = msg.find('\n', l)
    if l != -1 and r != -1:
        return msg[l:r].strip()
    return ""

def get_date(msg):
    l = msg.find('Date: ') + len('Date: ')
    r = msg.find('\n', l)
    if l != -1 and r != -1:
        return msg[l:r].strip()
    return ""

'''
Obtain boundary string of the email
'''
def get_boundary(content_type_header):
    boundary_start = content_type_header.find('boundary="') + len('boundary="')
    boundary_end = content_type_header.find('"', boundary_start)
    if boundary_start != -1 and boundary_end != -1:
        return content_type_header[boundary_start:boundary_end]
    else:
        return None

def get_subject(mssg):
    l = mssg.find('Subject: ') + len('Subject: ')
    r = mssg.find('\n', l)
    if l != -1 and r != -1:
        return mssg[l:r].strip()
    return ""

'''
Obtain the inline content from the raw email, which will be display in the email reader
'''
def get_inline(email_content):
    parts = email_content.split(f'--{get_boundary(email_content)}')
    cri = 'Content-Type: text/plain'
    this = ''
    for p in parts:
        if cri in p:
            this = p
            break
    
    # Define a regular expression pattern to match lines containing "Content-Type" or "Content-Disposition"
    pattern = r'^Content-Type:.*$|^Content-Disposition:.*$|Content-Transfer-Encoding:.*$|Subject:.*$'
    

    # Split the text by lines, filter out the matched lines, and join the remaining lines
    cleaned_text = '\n'.join(filter(lambda line: not re.match(pattern, line), this.split('\n')))

    # Remove empty lines
    cleaned_text = '\n'.join(filter(lambda x: x.strip(), cleaned_text.split('\n')))
    return cleaned_text

'''
Obtain the content of attachment from raw email content
'''
def get_attachment(email_content):
    parts = email_content.split(f'--{get_boundary(email_content)}')
    cri = 'Content-Disposition: attachment'
    att_list = []
    file_name = ''
    file_content = ''
    
    for p in parts:
        if cri in p:
            file_name_pattern = r'filename="([^"]+)"'
            file_name = re.findall(file_name_pattern, email_content)

            pattern = re.compile(r'Content-Transfer-Encoding: base64\s+([\w\s=+/]+)')
            matches = pattern.search(p)
            if matches:
                file_content = matches.group(1).strip()

            att_list.append((file_name, file_content))
    return att_list

def count_files(folder_path):
    return sum([1 for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
