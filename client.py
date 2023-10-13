import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
def connect(host, port):
	global s
	try:
		s.connect((host,port))
	except:
		print("Impossible de se connecter !")
		return None
	else:
		print(f"Connexion établie avec le serveur")
		return s

def envoie(s,m):
	message = m
	len_message = len(message)
	sent = 0
	while sent < len_message:
		sent += s.send(message.encode('utf-8'))
		if sent == 0:
			print('Envoi : Connexion rompue')
			break
		message = m[:sent]

	
	result = b''
	while result[-1:] != b'|':
		buff = s.recv(1)
		if not buff:
			print('Réception : Connexion rompue')
			return None
		result+= buff
	result = result.decode('utf-8')
	return result

def close():
	global s
	envoie(s,'STOP|')
	s.shutdown(0)
	s.close()
	print('FINI')

