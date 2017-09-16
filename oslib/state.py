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

import requests, logging
from .find import findff

class OSState:

    def __init__(self):
        self.baseurl = 'http://forum.outerspace.com.br/'
        self.session = requests.Session()
        self.token = ''
        self.data = ''
        self.url = ''

    def PrintCookies(self):
        logging.debug('Cookies (%d):' % len(self.session.cookies))
        for k, v in self.session.cookies.items():
            logging.debug(' %s: %s' % (k, v))

    def MakeUrl(self, url):
        return self.baseurl + url

    def GetUrl(self):
        return self.url

    def GetToken(self):
        return self.token

    def UpdateToken(self, data):
        token = findff(data, 
            '<input type="hidden" name="_xfToken" value="', '"')
        if token == None or token == '':
            logging.debug('Token not found!')
        else:
            self.token = token
            logging.debug("Got token '%s'." % self.token)

    def Get(self, url):
        url = self.MakeUrl(url)
        logging.debug('Requesting %s.' % url)
        res = self.session.get(url)
        self.url = res.url
        logging.debug("Response url is '%s'." % self.url)
        logging.debug('Response code is %d.' % res.status_code)
        self.data = res.text
        logging.debug('Response size is %d bytes.' % len(self.data))
        self.UpdateToken(self.data)
        return self.data

    def Post(self, url, data):
        url = self.MakeUrl(url)
        logging.debug('Requesting %s.' % url)
        res = self.session.post(url, data=data)
        self.url = res.url
        logging.debug("Response url is '%s'." % self.url)
        logging.debug('Response code is %d.' % res.status_code)
        self.data = res.text
        logging.debug('Response size is %d bytes.' % len(self.data))
        self.UpdateToken(self.data)
        return self.data

    def PostJSON(self, url, data):
        url = self.MakeUrl(url)
        logging.debug('Requesting %s.' % url)
        res = self.session.post(url, data=data)
        data = res.text
        json = res.json()
        logging.debug("Response url is '%s'." % res.url)
        logging.debug('Response code is %d.' % res.status_code)
        logging.debug('Response size is %d bytes.' % len(data))
        return json

