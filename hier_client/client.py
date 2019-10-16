import os
import sys
import argparse

import keyring
import anvil.server

from datetime import datetime
from functools import partial

from hier_client.__version__ import __version__

class Client:
    def __init__(self, dev_env=False):
        app_token = 'TK7FLRPXCNT5TQI44VM4KNCS-S2TS7IPRJHFHAPGR-CLIENT'
        if dev_env:
            app_token = 'JOX4D7EY52U45CSJD43DZT3U-P3WW7DFIISNFGUZK-CLIENT'
        self.user_email = keyring.get_password('Hier', 'user_email')
        if self.user_email is not None:
            self.password = keyring.get_password('Hier', self.user_email)
            if self.password is None:
                print('User email has been stored, but password has not. '
                      'Please regenerate token and rerun `hier init`.')
            else:
                print(app_token)
                anvil.server.connect(app_token, quiet=True)
                self.call = partial(
                    anvil.server.call,
                    user_email=self.user_email,
                    password=self.password
                )

    def initalize(self):
        user_email = input('Hier email: ')
        print('\n\nNOTE: '
              'Your password will be visible when you type/paste it. ',
              'But all credentials are stored securely using keyring.')
        password = input('Hier token: ')
        keyring.set_password('Hier', 'user_email', user_email)
        keyring.set_password("Hier", user_email, password)
        print('Credentials saved.')

    def user_pw_exist(self):
        exists = self.user_email is not None and self.password is not None
        if not exists:
            print('No user saved. Please run `hier init` first.')
        return exists

    def dev(self):
        return self.call('dev', datetime.now())

    def count_users(self):
        return self.call('count_users')

    def notes_by_users(self):
        return self.call('notes_by_users')

    def migrate_user_settings(self):
        return self.call('migrate_user_settings')

    def write(self, content, force=False, append=False):
        return self.call('write', content, force, append, datetime.now())

    def read(self):
        return self.call('read', datetime.now())

    def test(self):
        return self.call('test', datetime.now())

def run():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='', dest='command')
    parser_init = subparsers.add_parser('init', help='Initial setup.')

    # Admin
    parser_dev2 = subparsers.add_parser('dev2', help='Write full note.')
    parser_dev2.add_argument('--dev_env', '-d', action='store_true', help='Delete existing note. Replace with new content.')

    parser_count_users = subparsers.add_parser('count_users', help='Count number of users.')
    parser_notes_by_users = subparsers.add_parser('notes_by_users', help='Count number of notes, grouped by users.')
    parser_test = subparsers.add_parser('dev', help='Scratch endpoint.')
    parser_migrate_user_settings = subparsers.add_parser('migrate_user_settings', help='Refresh Users["settings"].')

    # Users
    parser_version = subparsers.add_parser('version', help='See what version of the client is installed.')
    parser_read = subparsers.add_parser('read', help='Read note(s).')
    parser_write = subparsers.add_parser('write', help='Write full note.')
    parser_write.add_argument('content', help='Note to save.')
    parser_write.add_argument('--force', '-f', action='store_true', help='Delete existing note. Replace with new content.')
    parser_write.add_argument('--append', '-a', action='store_true', help='Add content to an existing note.')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    allowed_args = set(('dev_env',))
    client_init_args = {k:v for k,v in vars(args).items() if k in allowed_args} # shrug
    client = Client(client_init_args)
    if args.command == 'init':
        client.initalize()
        return  # Early exit before verifying username exists.
    if not client.user_pw_exist():
        return
    elif args.command == 'dev2':
        print(client.dev())
    elif args.command == 'count_users':
        print(client.count_users())
    elif args.command == 'notes_by_users':
        for user, notes in client.notes_by_users():
            print(f"{user}: {notes}")
    elif args.command == 'migrate_user_settings':
        print(client.migrate_user_settings())
    elif args.command == 'write':
        print(client.write(args.content, args.force, args.append))
    elif args.command == 'read':
        print(client.read())
    elif args.command == 'test':
        print(client.test())
    elif args.command == 'version':
        print(__version__)

if __name__ == "__main__":
    run()
