#!/bin/env python
#coding=utf-8

import re
import os
import zipfile

'''
fileList = os.listdir('/home/chaos/script/pythonChallenge/channelZip')
path = '/home/chaos/script/pythonChallenge/channelZip'
first = '90052'
suffix = '.txt'
filename = first + suffix
regx = re.compile(r'[0-9]+')
f = open( os.path.join(path, filename), 'rb' )
string = f.read()
numList = re.findall(regx, string)
for num in numList:
    print num + suffix

for i in fileList:
    f = open( os.path.join(path, i), 'rb' )
    if not re.search('nothing', f.read() ):
        print os.path.join(path, i)

#    print os.path.join(path, i)
#    print f.read() '''

src_zipfile = zipfile.ZipFile('/home/chaos/script/pythonChallenge/channel.zip')
regx = re.compile(r'([0-9]{2,})')
string = src_zipfile.open('readme.txt').read()
try:
    num = re.search(regx, string).group(1)
except:
    pass

filelist = src_zipfile.namelist()
filelist.remove('readme.txt')
answer = ''
while True:
     if len(filelist) > 0:
        filename = num + '.txt'
        comment = src_zipfile.getinfo(filename).comment
        answer = answer + comment
        filecontent = src_zipfile.open(filename).read()
        try:
            num = re.search(regx, filecontent).group(1)
        except:
            pass
        filelist.remove(filename)
     else:
        break

print answer
