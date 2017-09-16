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

import logging, oslib, sys

###############################################################################
# Configure the log output format
###############################################################################

root = logging.getLogger()
root.setLevel(10)
root.handlers = []

ch = logging.StreamHandler(sys.stderr)
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(threadName)s - '+
    '%(levelname)s - %(message)s')

ch.setFormatter(formatter)

root.addHandler(ch)

###############################################################################
# Test
###############################################################################

logging.info('Hello!')

logging.info('Creating state object...')
state = oslib.OSState()

logging.info('Requesting index.php...')
data = state.Get('index.php')

logging.info('Response has %d bytes.' % len(data))

