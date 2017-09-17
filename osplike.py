#!/usr/bin/env python3

# MIT License
# 
# Copyright (c) 2017 Caian Benedicto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging, oslib, sys, getpass, argparse

###############################################################################
# Constants
###############################################################################

postbstr = '<div class="messageInfo primaryContent">'
postestr = '</form>'
lastpgfind = [
    ('+<div class="PageNav"', '>>'), 
    ('+data-last="', '>"')
]
postufind = [
    ('-<span class="authorEnd"><a href="index.php?members/', '>"'),
    ('+.', '>/')
]
postdfind1 = [
    ('-class="datePermalink"><span class="DateTime" title="', '>"')
]
postdfind2 = [
    ('-class="datePermalink"><abbr', '></a>'),
    ('+>', '><')
]
postifind = [
    ('-<div class="publicControls">', '></a>'),
    ('+data-href="index.php?posts/', '>/')
]
postlfind = [
    ('-class="LikeLabel">', '></span>')
]

notliked = 'Curtir'
liked = 'Curtir (remover)'

###############################################################################
# Command line arguments
###############################################################################

parser = argparse.ArgumentParser()

parser.add_argument('posts', help='Post ids separated by comma', nargs='?')
parser.add_argument('-i', '--stdin', help="Read list of posts from stdin (ignores the parameter 'posts')", action='store_true', default=False)
parser.add_argument('-r', '--rlike', help='Remove like', action='store_true', default=False)
parser.add_argument('-u', '--username', help='User name', default='')
parser.add_argument('-p', '--password', help='Password', default='')
parser.add_argument('-l', '--login', help='Interactive login', action='store_true', default=False)
parser.add_argument('-v', '--verbose', help='Verbosity level', type=int, choices=[0, 1, 2, 3], default=1)

args = parser.parse_args()

###############################################################################
# Configure the log output format
###############################################################################

root = logging.getLogger()
if args.verbose == 0:
    root.setLevel(100)
elif args.verbose == 1:
    root.setLevel(logging.ERROR)
elif args.verbose == 2:
    root.setLevel(logging.INFO)
else:
    root.setLevel(logging.NOTSET)
root.handlers = []

ch = logging.StreamHandler(sys.stderr)
ch.setLevel(logging.NOTSET)

formatter = logging.Formatter('%(asctime)s - %(threadName)s - '+
    '%(levelname)s - %(message)s')

ch.setFormatter(formatter)

root.addHandler(ch)

###############################################################################
# Program body
###############################################################################

logging.info('Hello!')

if args.posts == None:
    args.posts = ''

if args.stdin:

    if args.posts != '':
        sys.stderr.write('Post list cannot be used if reading from stdin!\n!')
        exit(1)

    if args.login:
        sys.stderr.write('Interactive login cannot be used if reading from stdin!\n!')
        exit(1)

else:

    if args.posts == '':
        sys.stderr.write('Not posts to like!\n!')
        exit(1)    

if args.login:

    connection = oslib.OSUser()

    login = input("Login: ")
    passw = getpass.getpass()

    logging.info("Logging in as '%s'..." % login)
    connection.Login(login, passw)

elif args.username != '' or args.password != '': 

    if args.username == '':
        sys.err.write('Password option requires the Username option to be set\n!')
        exit(1)

    if args.password == '':
        sys.err.write('Username option requires the Password option to be set\n!')
        exit(1)

    connection = oslib.OSUser()

    logging.info("Logging in as '%s'..." % args.username)
    connection.Login(args.username, args.password)

else:

    sys.stderr.write('Liking posts requires login!\n!')
    exit(1)

if not args.stdin:

    for pid in args.posts.split(','):
        if args.rlike:
            logging.info("Unliking post '%s'..." % pid)
            connection.Unlike(pid)
        else:
            logging.info("Liking post '%s'..." % pid)
            connection.Like(pid)

else:

    for line in sys.stdin:
        line = line.strip().split()
        for pid in line:
            if args.rlike:
                logging.info("Unliking post '%s'..." % pid)
                connection.Unlike(pid)
            else:
                logging.info("Liking post '%s'..." % pid)
                connection.Like(pid)

