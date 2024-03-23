import argparse
import socket
import json

BUFFER_SIZE = 8192000
SUFFIX = b"\x00\x00\x00\x00\x00"

def main():
    parser = argparse.ArgumentParser(description="Fast, reliable and easy-to-use file transfer CLI.")
    parser.add_argument("file", metavar="FILE", type=argparse.FileType("rb"), help="File (path) to send")
    parser.add_argument("host", metavar="HOST", type=str, help="Host IP to send to file to")
    parser.add_argument("--port", metavar="PORT", type=int, default=6567, help="Host port")

    args = parser.parse_args()

    file = args.file
    host = args.host
    port = args.port

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)

    try:
        print(f"Connecting to receiver...")
        sock.connect((host, port))
    except Exception as e:
        print(f"ERROR: {e}")
    
    sock.settimeout(120)

    file_content = file.read()
    request_data = {"name": file.name, "size": len(file_content)}

    sock.send(json.dumps(request_data).encode() + SUFFIX)

    print("Waiting for receiver to accept...")

    q_accept = sock.recv(1).decode()

    if not q_accept == "y":
        print(f"Receiver declined. Exiting...")
        return
    
    print("Receiver accepted. Sending file...")


    while file_content:
        sent = sock.send(file_content[:BUFFER_SIZE])

        file_content = file_content[sent:]
    
    print("Done!")

if __name__ == "__main__":
    main()
