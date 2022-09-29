import socket


port = 53533
ip = '192.168.1.208'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

while True:
    data, addr = sock.recvfrom(521)
    print('Print the data')
    print(data)
    # data = data.decode()
    # print(data)
    # data = json.loads(data)
    # print(data)
    # DNS registration
    if len(data) == 4:
        print('DNS register')
    # DNS query   
    elif len(data) == 2:
        print('DNS query')
    else:
        print('Error')










