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


from ETTTP_TicTacToe import TTT, check_msg
    
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
        else:
            print("메세지가 틀림")
            quit()
        ###################################################################
        
        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
