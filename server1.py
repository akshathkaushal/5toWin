import socket, select, sys, random

def broadcast_data(sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock:
            try:
                socket.send(message.encode())
            except:
                socket.close()
                CONNECTION_LIST.remove(socket)

if __name__ == "__main__":

    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    PORT = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setblocking(0)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(3)

    CONNECTION_LIST.append(server_socket)

    print "Chat server has started on port: " + str(PORT) + "\n"
    count = 0 
    a = []

    questions = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17', 'Q18', 'Q19', 'Q20']

    answers = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']

    points = {1: [], 2: [], 3: []}

    i = 19
    j = 1
    anscheck = 1
    while 1:
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])
        
        for sock in read_sockets:
            count = count + 1
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
                
                
                points[j].append(addr)
                h = 0
                points[j].append(h)
                j = j+1
                
                
                rules = str("\nThere will be 20 questions. A random question will appear on your screen each time. There are total 3 players out of which only one will be the winner.\nFor each question, the first person to press the buzzer ( Press 1 for the buzzer. ) will be given the chance to give the answer first. If his answer is correct, 1 point will be rewarded to him. In case he fails to give the correct answer the next player will be given the chance.The player who gets 5 points first will be declared as the winner.\nAll the very best.\n\n")

                
                x = str("Server: ")+str("Welcome to the game, here are the rules.\n")+rules
                if count == 3:
                    broadcast_data(sockfd, x)
                    sockfd.send(x)
    
                    number = random.randint(0,19)
                    if number not in a:
                        a.append(number)
                        broadcast_data(sockfd, str("Server: ")+str(questions[number])+str("\n"))
                        sockfd.send(str("Server: ")+str(questions[number])+str("\n"))
                    
            else:
                
                try:
                    buzzer = sock.recv(RECV_BUFFER)
                    ans = buzzer.decode()
                    
                    data = sock.recv(RECV_BUFFER)
                    data1 = (data.split('\n'))[0]
                    data2 = (data1.split(' '))[1]
                    if data:
                        
                        anscheck = 1
                        name = sock.getpeername()
                        broadcast_data(sock, "\r" + "<" + str(name) + ">   " + data.decode() + "\n")
                        print "(" + str(name) + ")   " + data.decode() + "\n"    
                        val = str(data2) == str(answers[number]) 
                        print val
                        

                        if val:
                            index = int((data.split(' '))[0]) 
                            points[index][1] = points[index][1] + 1 
                        
                        p1 = points[1][1]
                        p2 = points[2][1]
                        p3 = points[3][1]
                        
                        winner = "Congratulations! You have Won!!\n"
                        concl = "EndGame\n"

                        if p1==5:
                            result = "Client 1 has won.\n"
                            print result
                            broadcast_data(sock, result.encode())
                            sock.send(winner.encode())
                            broadcast_data(sock, concl.encode())
                            sock.send(concl.encode())
                            exit()
                        
                        elif p2==5:
                            result = "Client 2 has won.\n"
                            print result
                            broadcast_data(sock, result.encode())
                            sock.send(winner.encode())
                            broadcast_data(sock, concl.encode())
                            sock.send(concl.encode())
                            exit()
                        
                        elif p3==5:
                            result = "Client 3 has won.\n"
                            print result
                            broadcast_data(sock, result.encode())
                            sock.send(winner.encode())
                            broadcast_data(sock, concl.encode())
                            sock.send(concl.encode())
                            exit()


                        number = random.randint(0,19)
                        while number in a:
                            number = random.randint(0,19)
                        if number not in a:
                            a.append(number)
                            broadcast_data(sockfd, str("Server: ")+str(questions[number])+str("\n"))
                            sockfd.send(str("Server: ")+str(questions[number])+str("\n"))
                
                except:
                    #broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
         
    server_socket.close() 
