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

import logging
from .state import OSState
from .find import findff, findfr

class OSUser:

    def __init__(self):
        self.state = OSState()
        self.username = ''
        self.memberid = ''

    def SetUserInfo(self, data):
        self.username = findff(data, 
            '" class="username NoOverlay" dir="auto">', '<')
        if self.username == None or self.username == '':
            self.username = ''
            logging.debug('User name not found!')
        else:
            logging.debug("Got user name '%s'." % self.username)
        self.memberid = findfr(data, 
            '/" class="username NoOverlay"', '.')
        if self.memberid == None or self.memberid == '':
            self.memberid = ''
            logging.debug('Member id not found!')
        else:
            logging.debug("Got member id '%s'." % self.memberid)

    def GetByThread(self, threadid, page=1):
        return self.state.GetByThread(threadid, page)

    def GetByPost(self, postid):
        return self.state.GetByPost(postid)

    def Login(self, login, password):
        self.state.Get('index.php?login')
        res = self.state.Post('index.php?login/login', {
            'login': login,
            'password': password,
            'cookie_check': '1',
            'register': '0',
            'remember': '1',
            '_xfToken': self.state.GetToken(),
            'redirect': self.state.MakeUrl('index.php')
        })
        self.SetUserInfo(res)

    def LikeBase(self, postid, good, bad):
        res = self.state.PostJSON('index.php?posts/%s/like' % str(postid), {
            '_xfNoRedirect': '1',
            '_xfToken': self.state.GetToken(),
            '_xfRequestUri': self.state.GetUrl(),
            '_xfResponseType': 'json'
        })
        if res['term'] == good:
            logging.debug('Succeeded.')
            return True
        if res['term'] == bad:
            logging.error('Failed!')
            return False
        else:
            logging.error("Unknown response '%s'!" % res['term'])
            return None

    def Like(self, postid):
        good = 'Curtir (remover)'
        bad = 'Curtir'
        res = self.LikeBase(postid, good, bad)
        if res == True:
            return True
        if res == False:
            logging.debug('Ops, unliked the post, re-liking it...')
            if self.LikeBase(postid, good, bad) == True:
                return True
            else:
                return False
        else:
            logging.error("Unknown response '%s'!" % res['term'])
            return False

    def Unlike(self, postid):
        good = 'Curtir'
        bad = 'Curtir (remover)'
        res = self.LikeBase(postid, good, bad)
        if res == True:
            return True
        if res == False:
            logging.debug('Ops, liked the post, unliking it...')
            if self.LikeBase(postid, good, bad) == True:
                return True
            else:
                return False
        else:
            logging.error("Unknown response '%s'!" % res['term'])
            return False

