import os
import folder

'''
Load the existing history into program.
'''
def load():
    history_path = os.path.join(folder.get_user_dir(), 'history.txt')
    if not os.path.isfile(history_path):
        return []
    ls = []
    with open(history_path, 'r') as F:
        for line in F:
            if (len(line) == 0): continue
            ls.append(line.rstrip())
    return ls

'''
Write the email subject to the history file
'''
def write(line):
    history_path = os.path.join(folder.get_user_dir(), 'history.txt')
    with open(history_path, 'a') as f:
        f.write(line + '\n')
