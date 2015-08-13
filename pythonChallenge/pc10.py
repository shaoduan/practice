#!/bin/env python


from collections import OrderedDict
import re
import readline
import sys
# a = [1, 11, 21, 1211, 111221, 

def createstring(times):
    a = []
    a.append('1')
    while times > 0:
        string = a[-1]
        next_ = ''
#        string_set = set( list(string) )
        string_set = ''.join( OrderedDict.fromkeys(string) )
        for char in string_set:
            char_count = str( string.count(char) )
            next_ = next_ + char_count + char
            print 'times: %d' %times
            print 'char: %s, count: %s, next: %s' %(char, char_count, next_)
        a.append(next_)
        times = times - 1
    #print a[-1]
    return a




def create2(times):
    a = []
    a.append('1')
    while times > 0:
        string = a[-1]
        next_ = ''
        while len(string) > 0:
            char = string[0]
            regx = '%s{1,}' % char
            m = re.search(regx, string)
            chars_len = len( m.group() )
            next_ = next_ + str(chars_len) + char
            string = string[chars_len:]
        a.append(next_)
        times = times - 1
    return len(a[-1])

if len(sys.argv) != 2:
    print 'Please input only a number as argument.'
    exit(1)
print create2(times)
