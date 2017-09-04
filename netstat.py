#!/usr/bin/env python

import os

TCP = '/proc/net/tcp'
UDP = '/proc/net/udp'


def convHex2Dec(stringNum):
    #convert string Number provided to HEX
    dec = str(int(stringNum,16))
    return dec



def fetchData():
    with open(TCP,'r') as tcpData:
        data = tcpData.readlines()
        #remove the first line which is the header
        data.pop(0)
        return data


def getIP(data):
    A = convHex2Dec(data[6:8])
    B = convHex2Dec(data[4:6])
    C = convHex2Dec(data[2:4])
    D = convHex2Dec(data[0:2])
    return '.'.join([A,B,C,D])


def getSocket(data):
    host, port = data.split(':')
    return getIP(host), convHex2Dec(port)


tcpData = fetchData()


netstat = dict()

for line in tcpData:
    #split the line according to an empty space
    line = line.split(' ')
    #remove empty strings
    line = [x for x in line if x!='']
    
    #Local IP and Port
    lhost = getSocket(line[1])[0]
    lport = getSocket(line[1])[1]

    if lhost in netstat:
        netstat[lhost].append(lport)
    else:
        netstat[lhost] = [lport]

    #Remote IP and Port
#    rhost = getSocket(line[2])[0]
#    rport = getSocket(line[2])[1]
#    print (lhost + ':' + lport)
#    print (rhost + ':' + rport)
#    print netstat


for k, v in netstat.items():
    print k.ljust(16,'-') + '+'
    for item in v:
        print ' '.ljust(16)+ '|----'+ item
        
