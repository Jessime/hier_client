import os
import sys
import argparse
import getpass
import pkg_resources

import keyring
import requests


class Client:
    def __init__(self):
        self.base_url = "https://honorable-diligent-serval.anvil.app/_/api/"
        self.base_url = "https://joyful-shadowy-poet.anvil.app/_/api/"
        self.user_email = keyring.get_password('Hier', 'user_email')
        self.password = None
        self.auth = None
        if self.user_email is not None:
            self.password = keyring.get_password('Hier', self.user_email)
            self.auth = (self.user_email, self.password)

    def initalize(self):
        user_email = input('Hier email: ')
        password = getpass.getpass('Hier token: ')
        keyring.set_password('Hier', 'user_email', user_email)
        keyring.set_password("Hier", user_email, password)
        print('Credentials saved.')

    def count_users(self):
        url = self.base_url + 'count_users'
        response_text = requests.get(url, auth=self.auth).text
        return response_text

    def notes_by_users(self):
        url = self.base_url + 'notes_by_users'
        response_json = requests.get(url, auth=self.auth).json()
        return response_json

    def write(self, content, force=False, append=False):
        url = self.base_url + 'write'
        json = {'content': content, 'force': force, 'append': append}
        response_text = requests.post(url, auth=self.auth, json=json).text
        return response_text

    def read(self):
        url = self.base_url + 'read'
        response_text = requests.get(url, auth=self.auth).text
        return response_text

    def test(self):
        url = self.base_url + 'test'
        data = {'append': True}
        response_text = requests.post(url, auth=self.auth, json=data).text
        return response_text

def run():
    #formatter = argparse.ArgumentDefaultsHelpFormatter
    #parser = argparse.ArgumentParser(usage=USAGE, formatter_class=formatter)
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='', dest='command')
    parser_init = subparsers.add_parser('init', help='Initial setup.')

    # Admin
    parser_count_users = subparsers.add_parser('count_users', help='Count number of users.')
    parser_count_users = subparsers.add_parser('notes_by_users', help='Count number of notes, grouped by users.')
    parser_count_users = subparsers.add_parser('test', help='Scratch endpoint.')

    # Users
    parser_write = subparsers.add_parser('read', help='Read note(s).')
    parser_write = subparsers.add_parser('write', help='Write full note.')
    parser_write.add_argument('content', help='Note to save.')
    parser_write.add_argument('--force', '-f', action='store_true', help='Delete existing note. Replace with new content.')
    parser_write.add_argument('--append', '-a', action='store_true', help='Add content to an existing note.')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    if args.command == 'init':
        Client().initalize()
    elif args.command == 'count_users':
        print(Client().count_users())
    elif args.command == 'notes_by_users':
        for user, notes in Client().notes_by_users():
            print(f"{user}: {notes}")
    elif args.command == 'write':
        print(Client().write(args.content, args.force, args.append))
    elif args.command == 'read':
        print(Client().read())
    elif args.command == 'test':
        print(Client().test())

if __name__ == "__main__":
    run()
