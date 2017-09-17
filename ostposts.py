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

# List of formatting options:
# t - (t)hread id
# p - (p)ost id
# u - (u)ser id
# d - post (d)ate
# o - p(o)st number
# g - pa(g)e number
# l - (l)ike status, 1-liked, 0-not liked, x-not available (not logged or own post)

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

parser.add_argument('thread', help='Thread id')
parser.add_argument('-s', '--start', help='Starting page', type=int, default=1)
parser.add_argument('-e', '--end', help='Ending page (included)', type=int, default=None)
parser.add_argument('-f', '--format', help='Output table format', default='opu')
parser.add_argument('-u', '--username', help='User name', default='')
parser.add_argument('-p', '--password', help='Password', default='')
parser.add_argument('-l', '--login', help='Iterative login', action='store_true', default=False)
#parser.add_argument('-r', '--raw', help='Do not add padding to the columns', action='store_true', default=False)
parser.add_argument('-v', '--verbose', help='Verbosity level', type=int, choices=[0, 1, 2], default=2)

args = parser.parse_args()

###############################################################################
# Configure the log output format
###############################################################################

root = logging.getLogger()
if args.verbose == 2:
    root.setLevel(logging.ERROR)
elif args.verbose == 1:
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
# Test
###############################################################################
def tprint(format, tid, pid, uid, pdt, pon, pgn, like):
    s = []
    for f in format:
        # t - (t)hread id
        if f == 't':
            s.append(str(tid))
        # p - (p)ost id
        elif f == 'p':
            s.append(str(pid))
        # u - (u)ser id
        elif f == 'u':
            s.append(str(uid))
        # d - post (d)ate
        elif f == 'd':
            s.append(str(pdt))
        # o - p(o)st number
        elif f == 'o':
            s.append(str(pon))
        # g - pa(g)e number
        elif f == 'g':
            s.append(str(pgn))
        # l - (l)ike status
        elif f == 'l':
            s.append(str(like))
    print(' '.join(s))

###############################################################################
# Test
###############################################################################

def osdate(s):
    s = s.replace('às ', '')
    s = s.replace(' ', '-')
    s = s.replace('Janeiro', '01')
    s = s.replace('Fevereiro', '02')
    s = s.replace('Março', '03')
    s = s.replace('Abril', '04')
    s = s.replace('Maio', '05')
    s = s.replace('Junho', '06')
    s = s.replace('Julho', '07')
    s = s.replace('Agosto', '08')
    s = s.replace('Setembro', '09')
    s = s.replace('Outubro', '10')
    s = s.replace('Novembro', '11')
    s = s.replace('Dezembro', '12')
    return s

###############################################################################
# Test
###############################################################################

logging.info('Hello!')

if args.login:

    connection = oslib.OSUser()

    login = input("Login: ")
    passw = getpass.getpass()

    logging.info("Logging in as '%s'..." % login)
    connection.Login(login, passw)

elif args.username != '' or args.password != '': 

    if args.username == '':
        sys.err.write('Password option requires the Username option to be set!')
        exit(1)

    if args.password == '':
        sys.err.write('Username option requires the Password option to be set!')
        exit(1)

    connection = oslib.OSUser()

    logging.info("Logging in as '%s'..." % args.username)
    connection.Login(args.username, args.password)

else:

    connection = oslib.OSState()

#for pagenum in range(args.start, args.end + 1):
pagenum = 1 if args.start == None else args.start
pageend = args.end
page = connection.GetByThread(args.thread, pagenum)

if args.end == None:
    # Keep refreshing last page in case it changes
    # Find the last page using the PageNav
    pageend = int(oslib.superfind(page, lastpgfind))
    logging.debug('Last page is %d.' % pageend)

posti = 0
postidx = 1

while True:

    posti = page.find(postbstr, posti)
    if posti < 0:
        break

    postj = min(page.find(postestr), page.find(postbstr, posti+len(postbstr)))
    if postj < 0:
        # Should not happen
        postj = len(page)

    logging.debug('Post %d at [%d, %d].' % (postidx, posti, postj))

    post = page[posti:postj]
    pid = int(oslib.superfind(post, postifind))
    uid = int(oslib.superfind(post, postufind))
    like = oslib.superfind(post, postlfind)
    pdt1 = osdate(oslib.superfind(post, postdfind1))
    pdt2 = osdate(oslib.superfind(post, postdfind2))

    pdt = pdt1 if pdt1 != '' else pdt2

    if like == '':
        like = 'x'
    elif like == liked:
        like = '1'
    elif like == notliked:
        like = '0'

    tprint(args.format, args.thread, pid, uid, pdt, postidx, pagenum, like)

    posti = postj
    postidx += 1

logging.info('Found %d posts.' % (postidx-1))
