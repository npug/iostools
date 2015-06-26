#!/usr/bin/env python



import pexpect
import sys
import argparse


#Open and read config file






###Take arguments from CLI###
parser = argparse.ArgumentParser(description="test")
parser.add_argument('-ip', '--ipaddress', help='IP Address', required=True)
parser.add_argument('-u', '--user', help='username', required=True)
parser.add_argument('-p', '--password', help='password', required=True)
parser.add_argument('-l', '--line', help='line number', required=True)

args = parser.parse_args()

args.line = (str(args.line))
##Start using PEXPECT to interact with the router
session = pexpect.spawn('telnet ' + args.ipaddress)
session.logfile_read = sys.stdout

session.expect('.*Username: ')

session.sendline(args.user)
session.expect('Password: ')
session.sendline(args.password)

session.expect('.*>')
session.sendline('enable')

session.expect('Password: ')
session.sendline(args.password)

session.expect('.*#')
session.sendline('clear line %s' % args.line)

session.expect('[confirm]')
session.sendline('\n')

session.expect('.*#')
