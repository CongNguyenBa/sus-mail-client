import config, utils
import re

# Filter, which is responsible for filtering emails

class Filter:
    # Filter initialization
    def __init__(self):
        C = config.load()
        F = C['FILTER']
        self.content_filter = F['Content']['Which']
        self.subject_filter = F['Subject']['Which']
        self.from_filter = F['From']['Which']
        self.spam_filter = F['Spam']['Which']
    
    def filter_subject(self, content):
        subject_match = re.search(r"Subject:\s*(.*)", content)
        if subject_match:
            subject = subject_match.group(1)
        else: subject = ''
        
        subject = subject.lower()
        check = any(word in subject for word in self.subject_filter)
        if check:
            return True
        else: return False

    def filter_from(self, content):
        from_match = re.search(r"From:\s*(.*)", content)
        if from_match:
            from_add = from_match.group(1)
        else: from_add = ''

        check = any(word in from_add for word in self.from_filter)
        if check:
            return True
        else: return False
    
    def filter_content(self, content):
        content = content.lower()
        check = any(word in content for word in self.content_filter)
        if check: return True
        else: return False

    def filter_spam(self, content):
        content = content.lower()
        check = any(word in content for word in self.spam_filter)
        if check: return True
        else: return False

    def filter(self,content):
        C = config.load()
        F = C['FILTER']
        from_folder = F['From']['Folder']
        spam_folder = F['Spam']['Folder']
        subject_folder = F['Subject']['Folder']
        content_folder = F['Content']['Folder']

        inline_msg = utils.get_inline(content)
        
        if (self.filter_from(content)): return from_folder
        elif (self.filter_spam(inline_msg)): return spam_folder
        elif (self.filter_subject(inline_msg)): return subject_folder
        elif (self.filter_content(inline_msg)): return content_folder
        else: return 'Inbox'