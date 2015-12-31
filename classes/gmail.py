from imaplib import IMAP4_SSL
import email as em
from email.utils import parsedate, parsedate_tz
from email.parser import HeaderParser

class GmailAccount(object):
    def __init__(self, username=None, password=None, folder=None):
        self.username = username
        self.password = password
        self.folder = folder

    def login(self):
        self.conn = IMAP4_SSL('imap.gmail.com')
        response = self.conn.login(self.username, self.password)
        return response

    def search(self, query, folder=None, readonly=False):
        ff = self.folder if self.folder else folder
        self.conn.select(ff, readonly)
        resp, data = self.conn.search(None, query)
        return data

    def fetch(self, uids, query):
        uid_arr = b','.join(uids[0].split())
        resp, data = self.conn.fetch(uid_arr, query)
        return data

    def fetch_and_parse(self, uids, query):
        data = self.fetch(uids, query)
        parser = HeaderParser()
        emails = []

        for email in data:
            if len(email) < 2:
                continue
            msg = em.message_from_bytes(email[1]).as_string()
            emails.append(parser.parsestr(msg))

        return emails

    def load_parse_query(self, search_query, fetch_query, folder=None, readonly=False):
        '''Perform search and fetch on an imap Gmail account. After fetching relevant info
from fetch query, parse into a dict-like email object, return list of emails.'''
        uids = self.search(search_query, folder, readonly)
        return self.fetch_and_parse(uids, fetch_query)



def get_all_recips(parsed):
    if parsed['To'] and parsed['cc']:
        return parsed['To']+', '+parsed['cc']
    elif parsed['To']:
        return parsed['To']
    elif parsed['cc']:
        return parsed['cc']
    else: return None

def grab_email(string):
    '''assumes format 'First Last <some@thing.com>' '''
    return string.split('<')[-1][:-1]

def parse_from(email_dict, metadata):
    address = metadata.get('From').split('<')[-1][:-1]
    if address == None: return email_dict
    email_dict.setdefault(address, []).append(metadata)

def parse_to(email_dict, metadata):
    addressees = get_all_recips(metadata)
    if addressees == None: return email_dict
    #for each recipient in either the to or cc field:
    for to in addressees.split(','):
        email_dict.setdefault(grab_email(to), []).append(metadata)
    return email_dict
