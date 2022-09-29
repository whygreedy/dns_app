from flask import Flask, abort, request, Response
from socket import *
import json
import requests,socket

app = Flask(__name__)


@app.route('/')
def root():
    return 'Hello'


@app.route('/register', methods=['GET','PUT'])
def register():
    ServerReq = {
        'hostname' : request.args.get('hostname'),
        'ip' : request.args.get('ip'),
        'as_ip' : request.args.get('as_ip'),
        'as_port' : request.args.get('as_port')
    }
    return registerToAS(ServerReq)

def registerToAS(ServerReq):
    serverName = ServerReq['as_ip']
    serverPort = ServerReq['as_port']
    sock = socket(AF_INET,SOCK_DGRAM)
    msg = {
        'Type' : 'A',
        'Name' : str(ServerReq['hostname']),
        'Value' : str(ServerReq['ip']),
        'TTL' : 10
    }
    app_json = json.dumps(msg)
    sock.sendto(app_json.encode(),(serverName,int(serverPort)))
    response, serverAddress = sock.recvfrom(521)
    sock.close()
    response = response.decode()
    print('The response: ' + response)
    return "Done!",response

@app.route('/fibonacci')
def generateFib():
    seqNum = request.args.get('number')
    if not seqNum.isnumeric():
        abort(400)
    else:
        seqNum = int(seqNum)
        fibPre = 0
        fibCur = 1
        if seqNum > 0:
            for i in range(seqNum):
                temp = fibPre
                fibPre = fibCur
                fibCur = temp + fibCur
        return Response(str(fibPre), status = 200)


app.run(host='0.0.0.0',
        port=9090,
        debug=True)