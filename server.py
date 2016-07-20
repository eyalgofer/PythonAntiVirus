import socket
"""

how to test:
you can use which file you want' just drag it to AntiVirus folder and when asked fill the complete file name.
if you want to test with my files you can use "virus.txt" as a virus file and than use the signature based "1" form in client
with the signature file "virus_signature.txt" or use the "clean.pdf" file as a clean file that will be copied to client.

both files will reveal no viruses when sent to virus total.

"""
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
        data = conn.recv(1024) # receives a message from the client
        print('Server received', repr(data))
        filename = raw_input('Enter a file name: ') # get the name of file to send from the user.
        f = open(filename,'rb')
        l = f.read(1024)
        while (l): # sending file to client
           conn.send(l)
           l = f.read(1024)
        f.close()
        print('Done sending!')
        conn.close()

if __name__ == '__main__':
    main()