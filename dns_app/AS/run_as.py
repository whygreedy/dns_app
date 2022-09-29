from socket import *
import os
import json

port = 53533
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('', port))

while True:
    msg, addr = sock.recvfrom(521)
    msg = msg.decode()
    msg = json.loads(msg)
    print(msg)
    # DNS registration
    if len(msg) == 4:
        dnsfile = open("dnsdb.json", "w")
        addEntry = {
            msg['Name'] : msg
        }
        msg = json.dumps(addEntry)
        dnsfile.write(msg)
        dnsfile.close()
        sock.sendto(str(201).encode(),addr)
    # DNS query from US  
    elif len(msg) == 2:
        with open("dnsdb.json") as f:
           dnsmsg = json.loads(f)
        msg = dnsmsg[msg['Name']]
        msg = json.dumps(msg)
        sock.sendto(msg.encode(),addr)
    else:
        print("Error")











