import argparse
import socket
import json
import os

BUFFER_SIZE = 8192000
SUFFIX = b"\x00\x00\x00\x00\x00"

def recv_sock(sock: socket.socket):
    buffer = b""

    while True:
        data = sock.recv(1)

        if len(data) == 0:
            raise Exception("ERROR: Socket closed unexpectedly. Exiting...")
        
        buffer += data

        if buffer.endswith(SUFFIX):
            break

    return buffer.removesuffix(SUFFIX)

def main():
    if not os.path.exists("saved_files"):
        os.mkdir("saved_files")

    parser = argparse.ArgumentParser(description="Fast, reliable and easy-to-use file transfer CLI.")
    parser.add_argument("--host", metavar="HOST", type=str, default="0.0.0.0", help="Listening host")
    parser.add_argument("--port", metavar="PORT", type=int, default=6567, help="Listening port")

    args = parser.parse_args()

    host = args.host
    port = args.port

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()

    print("Waiting for sender to connect...")

    sender_sock, sender_address = sock.accept()

    try:
        request_data = json.loads(recv_sock(sender_sock).decode())
    except Exception as e:
        print(e)
        return
    
    filename = request_data["name"]
    filesize = request_data["size"]

    print(f"File request received: Name: {filename} Size: {filesize} bytes")

    if os.path.exists(f"./saved_files/{filename}"):
        q_file_exists = input(f"File ./saved_files/{filename} already exists. Overwrite? [Y/n]: ").lower()

        if not q_file_exists == "y":
            sender_sock.send("n".encode())
            print(f"Declied! Exiting...")
            return
        
        else:
            os.remove(f"./saved_files/{filename}")
        
    else:
        q_accept = input(f"Sender connected ({sender_address[0]}:{sender_address[1]}), accept? [Y/n]: ").lower()

        if not q_accept == "y":
            sender_sock.send("n".encode())
            print("Declined! Exiting...")
            return

    sender_sock.send("y".encode())

    print("You have accepted. Receiving file...")

    file_buffer = b""

    while True:
        data = sender_sock.recv(BUFFER_SIZE)

        if len(data) == 0:
            print(f"ERROR: Socket closed unexpectedly. Exiting...")
            return
        
        file_buffer += data

        if len(file_buffer) == filesize:
            break
    
    file_content = file_buffer.removesuffix(SUFFIX)

    with open(f"./saved_files/{filename}", "wb") as file:
        file.write(file_content)
        file.close()
        
if __name__ == "__main__":
    main()
