#!/usr/bin/env python

import os
import sys

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


def findPIDs():
    #create a list with the file/folder contents of /proc
    processFiles = os.listdir("/proc/")
    
    #remove the ProcessID of the current Process
    processFiles.remove(str(os.getpid()))

    #create a list with process id files
    pids = []

    for filename in processFiles:
        try:
             #convert the filename to integer and append it to the pids list if it's a pid
             integer = int(filename)
             pids.append(str(integer))

        except ValueError:
             #if the filename doesn't convert to integer it's not a pid. Skip it.
             pass

    return pids

def findInode(inode, pids):

     #use the created pids list
     for pid in pids:
         #list dir for each process id to get the File Descriptors 
         fDescriptors = os.listdir('/proc/%s/fd/' %pid)
        
         #for each pid and filedescriptor search for the socket with the relave Inode
         for fd in fDescriptors:
             pidFile = '/proc/%s/fd/%s' % (pid, fd)
             #dereference symbolic link and check if it is equal to the inode
             if os.path.exists(pidFile):
                 if os.readlink(pidFile) == ('socket:[%d]' %inode):
                     return pid

    
def getprocessName(pid):
    if pid:
        path = '/proc/' + pid + '/comm'
        with open(path, 'r') as cmdFile:
            return cmdFile.read().strip('\n')
    return None



if not os.geteuid() == 0:
        sys.exit('Become root and try again!\nExiting...')


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

    #Acquire CONNECTION STATE from line
    state = State[line[3]]
    
    #Acquire Inode from line
    inode = int(line[9])
    
    pids = findPIDs()
    pid  = findInode(inode ,pids)
   
    #prepare the Dictionary
    datList = [[lport, state, pid]]
    if lhost in netstat:
        netstat[lhost].append(datList)
    else:
        netstat[lhost] = [datList]


for key, values in netstat.items():
    print key.ljust(16,'-') + '+'
    for item in values:
      
        print ' '.ljust(16)+ '|----> '+ 'port:'+ str(item[0][0]).ljust(10) + ' '\
                + str(item[0][1]) + ' PID:' + str(item[0][2]) + ' NAME:' \
                + getprocessName(item[0][2]) 
