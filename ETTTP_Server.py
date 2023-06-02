'''
  ETTTP_Sever_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

import random
import tkinter as tk
from socket import *
import _thread

def check_msg(msg, ip):
    expected_ip="127.0.0.1"
    try:
        #message가 형식에 맞는지 확인
        type, etttp, host, action=map(str, msg.split())

        #ip가 제대로 작성되었는지 확인
        if ip!=expected_ip:
            return False

        #send와 ack 맞는지 확인
        if type not in ("SEND", "ACK", "RESULT"):
            return False

        #ETTTP이고, 버전이 맞는지 확인
        if etttp!="ETTTP/1.0":
            return False
    
        #호스트가 올바르고 구문이 맞는지 확인
        if host!="Host:"+expected_ip:
            return False
        
        #new move가 0과 2 사이이고 구문이 맞는지 확인
        if type in ("SEND", "ACK") and action.startswith("New-Move:(") and action.endswith(")"):
            a,b = map(str, action[10:-1].split(","))
            if 0<=int(a)<=2 and 0<=int(b)<=2:
                return True
        elif type =="RESULT" and action.startswith("Winner:"):
            winner= action[7:]
            if winner in ("ME", "YOU"):
                return True
        elif type =="SEND" and action.startswith("First-Move:"):
            first_turn=action[11:]
            if first_turn in ("ME", "YOU"):
                return True
        return False
    except Exception as e:
        return False
        

#from ETTTP_TicTacToe_skeleton import TTT, check_msg
    
if __name__ == '__main__':
    
    global send_header, recv_header

    SERVER_PORT = 12000
    SIZE = 1024
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',SERVER_PORT))
    server_socket.listen()
    MY_IP = '127.0.0.1'
    
    while True:
        client_socket, client_addr = server_socket.accept()
        
        start = random.randrange(0,2)   # select random to start
        if start==0: 
            start_user = "ME"
        else:
            start_user = "YOU"
        ###################################################################
        # Send start move information to peer
        start_move_message = f'SEND ETTTP/1.0\r\nHost:{MY_IP}\r\nFirst-Move:{start_user}\r\n\r\n'
        client_socket.sendall(start_move_message.encode())

        start_index = start_move_message.index("First-Move:") + len("First-Move:")
        substring = start_move_message[start_index:]

        # Receive ack - if ack is correct, start game
        ack_message = client_socket.recv(SIZE).decode().strip()
        ###################################################################

        if check_msg(ack_message, MY_IP): 
            pass
            # root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
            # root.play(start_user=start)
            # root.mainloop()

        client_socket.close()
        
        break
    server_socket.close()
