'''
  ETTTP_Client_skeleton.py
 
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

    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)

    
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)
        
        ###################################################################
        # Receive who will start first from the server
        start_move_message = client_socket.recv(SIZE).decode().strip()
        check_result = (check_msg(start_move_message, MY_IP))

        start_index = start_move_message.index("First-Move:") + len("First-Move:")
        start_user = start_move_message[start_index:]

        if start_user=="ME": 
            print("서버 선")
            start=0
        else: 
            print("클라이언트 선")
            start=1

        # etttp에 맞는 형식인 것을 확인하고 Send ACK 
        if check_result:
            ack_message ="ACK"+start_move_message[4:]
            client_socket.sendall(ack_message.encode())
        ###################################################################
        
        # Start game
        # root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        # root.play(start_user=start)
        # root.mainloop()
        client_socket.close()

        
