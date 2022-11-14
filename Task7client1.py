# local client for chat

import socket
import sys
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect(("127.0.0.1", 8888))
except ConnectionRefusedError:
    sys.exit("Error. Connection refused.")
else:
    print("connected. Wait a bit. Your joining is in progress")
    msg1 = sock.recv(1024).decode("utf-8")
    print(msg1)
    name = input("What is your name? ").upper()

stop_thread = threading.Event()
count = 0   # needed to make threading stop


def close():
    return sock.close()


def msg_came():
    global count
    while True:
        msg = sock.recv(1024).decode("utf-8")
        if msg == "exit":
            if stop_thread.is_set():
                close()
                count = 1
                break
        print(msg)


def send_msg(name):
    global count
    while True:
        if count == 1:
            break
        else:
            your_message = input()
            if your_message == "exit":
                sock.send(b"exit")
                count = 1
                if stop_thread.is_set():
                    return close()
            else:
                named_msg = (name + ":" + " " + your_message).encode("utf-8")
                return sock.send(named_msg)


while True:
    thread1 = threading.Thread(target=msg_came)
    thread1.start()
    thread2 = threading.Thread(target=send_msg, args=(name,))
    thread2.start()
    if count == 1:
        stop_thread.set()
        thread2.join()
        thread1.join()
