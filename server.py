import socket

def main():
    port = 60004                    # Reserve a port
    s = socket.socket()             # Create a socket
    host = socket.gethostname()     # Get local machine name
    s.bind((host, port))            # Bind to the port
    s.listen(5)                     # Wait for client connection.

    print 'Server listening....'
    while True:
        conn, addr = s.accept()     # Establish a connection with client.
        print 'Got connection from', addr
        data = conn.recv(1024)
        print('Server received', repr(data))
        filename = raw_input('Enter a file name: ')
        f = open(filename,'rb')
        l = f.read(1024)
        while (l):
           conn.send(l)
           l = f.read(1024)
        f.close()
        print('Done sending!')
        conn.close()

if __name__ == '__main__':
    main()