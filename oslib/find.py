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

def strfind(s, t, i=0):
    return s.find(t, i)

def strrfind(s, t, i=0):
    if i == 0:
        i = len(s)
    return s.rfind(t, 0, i)

def find(data, tokeni, tokenj, k, funci, funcj):
    i = funci(data, tokeni, k)
    if i < 0:
        return None
    i = i + len(tokeni)
    j = funcj(data, tokenj, i)
    if i <= j:
        a = i
        b = j
    if i > j:
        i = i - len(tokeni)
        j = j + len(tokenj)
        b = i
        a = j
    return data[a:b]

def findff(data, tokeni, tokenj, k=0):
    return find(data, tokeni, tokenj, k, strfind, strfind)

def findfr(data, tokeni, tokenj, k=0):
    return find(data, tokeni, tokenj, k, strfind, strrfind)

def findrf(data, tokeni, tokenj, k=0):
    return find(data, tokeni, tokenj, k, strrfind, strfind)

def findrr(data, tokeni, tokenj, k=0):
    return find(data, tokeni, tokenj, k, strrfind, strrfind)

