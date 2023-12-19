import os
import config

'''
----- FOLDER OPERATOR -----

'''

'''
Create all mailbox-related folders if not available
'''
def init_folder():
    C = config.load()
    if not os.path.isdir(f'{get_user_dir()}'):
        os.mkdir(f'{get_user_dir()}')
    if not os.path.isdir(get_mailbox_dir()):
        os.mkdir(get_mailbox_dir())
    if not os.path.isdir(get_attachment_dir()):
        os.mkdir(get_attachment_dir())

    inbox_folder = f'{get_mailbox_dir()}\\Inbox'
    if not os.path.isdir(inbox_folder):
        os.mkdir(inbox_folder)

    for folder in C['FILTER']:
        name = C['FILTER'][folder]['Folder']
        path = os.path.join(get_mailbox_dir(), name)
        if not os.path.isdir(path):
            os.mkdir(path)

'''
Get list of subfolders
Used for browsing mailbox
'''
def get_subfolder_list():
    return [name for name in os.listdir(get_mailbox_dir())
        if os.path.isdir(os.path.join(get_mailbox_dir(), name))]

'''
Get the mailbox directory from anywhere
'''
def get_mailbox_dir():
    C = config.load()
    return f'{C['USERNAME']}\\Mailbox'

'''
Get the user directory
'''
def get_user_dir():
    C = config.load()
    return f'{C['USERNAME']}'

'''
Get the attachment directory
'''
def get_attachment_dir():
    C = config.load()
    return f'{C['USERNAME']}\\Attachments'