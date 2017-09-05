#!/usr/bin/env python

import os

TCP = '/proc/net/tcp'
UDP = '/proc/net/udp'

State = {
        '01':'ESTABLISHED',
        '02':'SYN_SENT',
        '03':'SYN_RECV',
        '04':'FIN_WAIT1',
        '05':'FIN_WAIT2',
        '06':'TIME_WAIT',
        '07':'CLOSE',
        '08':'CLOSE_WAIT',
        '09':'LAST_ACK',
        '0A':'LISTEN',
        '0B':'CLOSING'
        } 

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


#instantiate a Dictionary to hold
#lists of values per IP
netstat = dict()

for line in tcpData:
    #split the line according to an empty space
    line = line.split(' ')
    #remove empty strings
    line = [x for x in line if x!='']
    
    #Local IP and Port
    lhost = getSocket(line[1])[0]
    lport = getSocket(line[1])[1]

    state = State[line[3]]



    #prepare the Dictionary
    datList = [[lport,state]]
    if lhost in netstat:
        netstat[lhost].append(datList)
    else:
        netstat[lhost] = [datList]


for key, values in netstat.items():
    print key.ljust(16,'-') + '+'
    for item in values:
        print ' '.ljust(16)+ '|----> '+ str(item[0][0]) +' ' + str(item[0][1])