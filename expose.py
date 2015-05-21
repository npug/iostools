#!/usr/bin/env python2

###this is a simple script i created for my own lab to open a port on my router and forward it
###to something in my lab behind NAT.  Currently very basic, but pretty useful.  Just edit
###expose.cfg the first time, OR make sure you use the -n -l -p arguements the first time to prime
###the config

###I left the logging on.  You can disable this by removing session.logfile_read = sys.stdout



import pexpect
import sys
import argparse
import yaml


#Open and read config file
file = open("expose.cfg", 'r')
config = yaml.load(file)
file.close()





###Take arguments from CLI###
parser = argparse.ArgumentParser(description="test")
parser.add_argument('-ia', '--insideaddress', help='Inside address', required=True)
parser.add_argument('-ip', '--insideport', help='Inside Port', required=True)
parser.add_argument('-op', '--outsideport', help='Outside Port', required=True)
parser.add_argument('-oa', '--outsideaddress', help='Outside Address', required=False)
parser.add_argument('-n', '--host', help='Host IP', required=False)
parser.add_argument('-l', '--user', help='username', required=False)
parser.add_argument('-p', '--password', help='password', required=False)

args = parser.parse_args()

outsideaddress = ""
if args.outsideaddress == None:
    if args.host != None:
        outsideaddress = args.host
    elif config['host'] != None:
        outsideaddress = config["host"]
else:
    outsideaddress = args.outsideaddress

user = ""
if args.user == None:
    if config['user'] != None:
        user = config['user']
else:
    user = args.user

password = ""
if args.password == None:
    if config['pass'] != None:
        password = config['pass']
else:
    password = args.password

host = ""
if args.host == None:
    if config['host'] != None:
        host = config['host']
else:
    host = args.host





##Build IOS Commands to add
if config['nat'] == None:
    oldnatcommand = ""
else:
    oldnatcommand = config['nat']

newnatcommand = 'ip nat inside source static tcp ' + args.insideaddress + ' ' + args.insideport + ' ' + outsideaddress + ' ' + args.outsideport + ' extendable'


##Start using PEXPECT to interact with the router
session = pexpect.spawn('telnet ' + host)
session.logfile_read = sys.stdout

#session.expect('.*Username: ')

#session.sendline(user)
session.expect('Password: ')
session.sendline(password)

session.expect('.*>')
session.sendline('enable')

session.expect('Password: ')
session.sendline(password)

session.expect('.*#')
session.sendline('conf t')

session.expect('.*#')
session.sendline('no ' + oldnatcommand)

session.expect('.*#')
session.sendline(newnatcommand)

session.expect('.*#')



###Write new config to file, for easy command removal, and if you use the same router multiple times, less args to input
new_config = {}
new_config['host'] = host
new_config['user'] = user
new_config['pass'] = password
new_config['insideaddress'] = args.insideaddress
new_config['insideport'] = args.insideport
new_config['outsideport'] = args.outsideport
new_config['outsideaddress'] = outsideaddress
new_config['nat'] = newnatcommand

###write new config file
file = open('expose.cfg', 'w')
file.write(yaml.dump(new_config, default_flow_style=False))
file.close()