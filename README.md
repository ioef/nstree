# nstree

A useful utility which shows an equivalent to sudo netstat -pant in a pstree like structure.

usage: sudo ./nstree.py

Example:
```
sudo ./nstree.py 
0.0.0.0---------+
                |----> port:113        LISTEN PID:718 NAME:inetd
                |----> port:445        LISTEN PID:1198 NAME:smbd
                |----> port:59166      LISTEN PID:691 NAME:rpc.statd
                |----> port:139        LISTEN PID:1198 NAME:smbd
                |----> port:111        LISTEN PID:682 NAME:rpcbind
127.0.0.1-------+
                |----> port:631        LISTEN PID:833 NAME:cupsd
                |----> port:25         LISTEN PID:1928 NAME:exim4
                |----> port:9050       LISTEN PID:883 NAME:tor
                |----> port:3306       LISTEN PID:1414 NAME:mysqld
```

