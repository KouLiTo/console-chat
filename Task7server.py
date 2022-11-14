# localhost for chat

import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_adress = ("127.0.0.1", 8888)
sock.bind(server_adress)

sock.listen()
print("waiting for connections")

members = []


def new_member(member):             # initialize a new member
    print("New member connected")
    member.send(b"You joined the chat")
    return member


def send_all(msg):                  # func sends transfers messages into the chat room
    global members
    for member in members:
        member.send(str(msg).encode())


def exit_member(member):            # deleting a member from chat if exit executed by a member
    global members
    if member in members:
        member.send(b"exit")
        members.remove(member)
        send_all("One person left the chat")


def msg_came(member):                 # func processing incoming messages onto the server
    if member in members:
        while True:
            msg = member.recv(1024).decode("utf-8")
            if msg:
                if msg == "exit":
                    exit_member(member)
                else:
                    send_all(msg)
            else:
                raise ConnectionError("Something went wrong")

while True:
    member, adress = sock.accept()     # save member's info
    member = new_member(member)
    members.append(member)             # append a new member to the server list
    thread = threading.Thread(target=msg_came, args=(member,))    # module coordinates multythreading
    thread.start()


