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

from ETTTP_TicTacToe_skeleton import TTT, check_msg
    
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
        #start_move_info = start_move_message.split('\r\nFirst-Move: ')[1].split('\r\n')[0]
        check_reuslt = (check_msg(start_move_message, MY_IP))


        if check_reuslt:
            ack_message ="ACK"+start_move_message[4:]
            client_socket.sendall(ack_message.encode())

        # Send ACK 
        #ack_message = 'ACK ETTTP/1.0\r\nHost: {}\r\n\r\n'.format(MY_IP)
        #client_socket.sendall(ack_message.encode())
        ###################################################################
        
        # Start game
        #root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        #root.play(start_user=start)
        #root.mainloop()
        client_socket.close()
        
        
