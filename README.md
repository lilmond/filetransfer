# filetransfer
Fast, reliable and easy-to-use file transfer CLI.

## BASIC USAGE
> [!NOTE]
> Default listening port of receiver is 6567.

### Sender
```
usage: send.py [-h] [--port PORT] FILE HOST

Fast, reliable and easy-to-use file transfer CLI.

positional arguments:
  FILE         File (path) to send
  HOST         Host IP to send to file to

options:
  -h, --help   show this help message and exit
  --port PORT  Host port
```
Example:
```
python send.py teddy.png 127.0.0.1
```

### Receiver
```
usage: receive.py [-h] [--host HOST] [--port PORT]

Fast, reliable and easy-to-use file transfer CLI.

options:
  -h, --help   show this help message and exit
  --host HOST  Listening host
  --port PORT  Listening port
```
Example:
```
python receive.py
```
