import socket
import threading, time


host = ''
port = 8080
connexions = {}
messages_attente = {}

def worker(c,addr,idd):
	pseudo = f'{addr[0]}:{addr[1]}'
	while True:
		commandes_attente = []
		#Réception et traitement infos
		data = b''
		while data[-1:] != b'|':
			
			buff = c.recv(1)
			if buff == b'':
				print('Réception : Connexion rompue')
				return None
			data+= buff
		data = data.decode('utf-8')
		#data = c.recv(512)
		#data = data.decode('utf-8')
		if not data:
			for i in messages_attente:
				if i != idd:
					messages_attente[i].append(f'Connexion perdue avec {pseudo} ')
			print(f"Connexion avec {pseudo} rompue")
			close(c,False)
			break
		else:
			data = data[:-1]


		if data == "STOP":
			c.sendall("OK|".encode('utf-8'))
			for i in messages_attente:
				if i != idd:
					messages_attente[i].append(f'{pseudo} s\'est déconnecté ')
			close(c,False)
			break
		elif data == 'STOPSERV':													  
			for i in messages_attente:
				if i != idd:
					messages_attente[i].append('Extinction du serveur')
			time.sleep(1)
			close(c,True)
			break
		elif data.startswith("PSEUDO"):
			data = data.split(":")[1]
			pseudo = data
			for i in messages_attente:
				if i != idd:
					messages_attente[i].append(f'{pseudo} vient de se connecter')
			c.sendall("OK|".encode('utf-8'))
		elif data == 'UPDATE':
			if messages_attente[idd] != []:
				c.sendall((";".join(messages_attente[idd])+'|').encode('utf-8'))
				messages_attente[idd] = []
			else:
				c.sendall("OK|".encode('utf-8'))					
		else:
			for i in messages_attente:
				if i != idd:
					messages_attente[i].append(f'{pseudo} : {data}')
			c.sendall("OK|".encode('utf-8'))
		time.sleep(0.01)
	print("thread killed")
	
def close(c,serv):
	global s
	c.shutdown(0)
	c.close()
	if serv :
		#s.shutdown(0)
		s.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
print("Serveur démarré\nEn attente de requêtes...")
while True:
	s.listen(1)
	try:
		conn, addr = s.accept()
	except:
		break
	connexions[len(connexions)] = (conn,addr)
	messages_attente[len(connexions)] = []
	new_thread = threading.Thread(target = worker, args=(conn,addr,len(connexions)))
	new_thread.start()
	print(f"Nouvelle connexion avec {addr[0]}:{addr[1]}, id : {len(connexions)}")
print("Serveur éteint")
