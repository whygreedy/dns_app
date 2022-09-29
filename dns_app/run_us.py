from flask import Flask, abort, request
from socket import *
import json
import requests,socket

app = Flask(__name__)


@app.route('/')
def root():
    return 'Please refer to /fibonacci'

@app.route('/fibonacci')
def Path():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    seqNum = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
    if hostname == None or fs_port == None or seqNum == None or as_ip == None or as_port == None:
        abort(400) # Bad Request
    
    # Send DNS query to AS via UDP msg
    sock = socket(AF_INET,SOCK_DGRAM)
    msg = {
    'Name' : hostname,
    'Type' : 'A'
    }
    msg = json.dumps(msg)
    sock.sendto(msg.encode(),(as_ip,int(as_port)))

    # Receive DNS query results from AS 
    replyMsg,server = sock.recvfrom(521)
    replyMsg = replyMsg.decode()
    if replyMsg == 'DNS not found.':
        abort(400)
    replyMsg = json.loads(replyMsg)

    # Display the results from FS
    url = 'http://'+replyMsg['Value']+':'+fs_port+'/fibonacci?number='+seqNum
    print(url)
    r = requests.get(url)
    return r.text

app.run(host='0.0.0.0',
        port=8080,
        debug=True)