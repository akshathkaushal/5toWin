import socket, select, string, sys

def prompt():
    #sys.stdout.write('--> ')
    sys.stdout.flush()


if __name__ == "__main__":
    if len(sys.argv)<3:
        print "Usage: python chat_client.py hostname port."
        sys.exit()
    
    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try:
        s.connect((host, port))
    except:
        print "Unable to connect to server."
        sys.exit()
    print "\nHello Player 3\n"
    print "Connected to the server."
    #prompt()

    while 1:
        socket_list = [sys.stdin, s]

        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for sock in read_sockets:
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    print "\nConnection terminated."
                    sys.exit()
                else:
                    prompt()
                    sys.stdout.write(data.decode())
                    data = (data.split('\n'))[0]
                    if data == "EndGame":
                        sys.exit()
            else:
                prompt()
                msg = sys.stdin.readline()
                s.send(str("3 ")+msg.encode())
