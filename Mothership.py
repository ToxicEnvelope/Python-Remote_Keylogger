import socket
import threading

def handle_check_in(incoming, addr):
   print '[*] Got connection from Seedship at :', addr
   file_from_seed = incoming.recv(1024)
   newFile = open(file_from_seed, 'a+')
   print "=> Receiving File from Seedship"
   while True:
		size = int(incoming.recv(16))
		recvd = ''
		while size > len(recvd):
			data = incoming.recv(1024)
			newFile.write(data)
			if not data: 
			    break
			recvd += data
		incoming.send('File transfer complete')
		newFile.close()
		break
   print "[*] File transfer complete from" , addr
   incoming.close()


print "[+] Mothership server is up"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 22555
host = '192.168.1.28'
s.bind((host, port))
s.listen(5)
while True:
   conn, addr = s.accept()
   babyship = threading.Thread(target=handle_check_in, args=(conn, addr))
   babyship.start()

