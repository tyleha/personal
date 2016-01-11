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
