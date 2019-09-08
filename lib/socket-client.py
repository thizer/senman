import socket

HOST = 'pernalonga.LooneyTunes'
PORT = 1987

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

print 'Type \'exit\' to... You know... '

# Wait for the first command
msg = raw_input()

while True:

    # Send to the server
    tcp.send(msg)
    
    # Exit if was requested to 
    if (msg == 'exit'):
        break

    # Wait for next command
    msg = raw_input()

tcp.close()

