from datetime import datetime
import random 
import json
import os
import shutil
import requests

# Petite aide pour colorer le texte dans le terminal (codes ANSI)
def colored(text: str, color_code: str) -> str:
    return f"\033[{color_code}m{text}\033[0m"

class User:
    def __init__(self, name: str, id: str): #crétion de la classe User qui contient tous les élements du dico users
        self.name = name
        self.id = id
    def __repr__(self) -> str:
  #'''Appelée lors de la conversion d'une instance de la classe `User` en `str`. C'est le cas lorsqu'on `print` une instance.'''
        return f'User(name={self.name})'
    

class Channel:
    def __init__(self, name: str, idg: int,members : list): #crétion de la classe Channel qui contient tous les élements du dico channels
        self.name = name
        self.idg = idg
        self.members = members
    def __repr__(self) -> str:
  #'''Appelée lors de la conversion d'une instance de la classe `Channel` en `str`. C'est le cas lorsqu'on `print` une instance.'''
        return f'Channel(name={self.name}, members {self.members})'

class Message:
    def __init__(self, channel: int, id: int,content : list[str], time : str, sender : int): #crétion de la classe Message qui contient tous les élements du dico messages
        self.channel = channel
        self.id = id
        self.content = content
        self.time = time
        self.sender = sender
    
    def __repr__(self) -> str:
  #'''Appelée lors de la conversion d'une instance de la classe `Message` en `str`. C'est le cas lorsqu'on `print` une instance.'''
        return f'Message(Content={self.content})'

class RemoteStorage: 
    def get_users(self)-> list[User]:
        liste = []
        response = requests.get("https://groupe5-python-mines.fr/users")
        for dico in response.json():
            liste.append(User(dico['name'],dico['id']))
        return liste
    
    def create_user(self,name :str)-> int :
        user = {'name' : name}
        response = requests.post("https://groupe5-python-mines.fr/users/create",json = user)
        return response.json()['id']

    def get_channel(self)-> list[User]:
        liste = []
        response = requests.get("https://groupe5-python-mines.fr/channels")
        print(response.json())
        for dico in response.json():
            members = requests.get(f"https://groupe5-python-mines.fr/channels/{dico['id']}/members").json()
            print(members)
            liste.append(Channel(dico['name'],dico['id'],members))
            print(Channel(dico['name'],dico['id'],members))  
        return liste
    def create_channel(self,name, id_channel):
        channel = {'name' : name, 'id' : id_channel }
        requests.post("https://groupe5-python-mines.fr/channels/create",json = channel)
        print(requests.post("https://groupe5-python-mines.fr/channels/create",json = channel))
    
    def add_user_channel(self,user_id ,id_channel):
        user = {'user_id' : user_id}
        post_user = requests.post(f"https://groupe5-python-mines.fr/channels/{id_channel}/join",json = user )
        print(post_user.text)
    
    def get_message(self)-> list[User]:
        liste = []
        response = requests.get("https://groupe5-python-mines.fr/messages")
        for dico in response.json():
            liste.append(Message(dico['channel_id'],dico['id'], dico['content'], dico['reception_date'], dico['sender_id']))
        return liste
    
    def get_channel_message(self, id_channel)-> list[User]:
        liste = []
        response = requests.get(f"https://groupe5-python-mines.fr/channel/{id_channel}/messages")
        for dico in response.json():
            liste.append(Message(dico['channel_id'],dico['id'], dico['content'], dico['reception_date'], dico['sender_id']))
        return liste

    def create_message(self,id_channel, content, sender_id):
        message = {'sender_id':sender_id, 'content' : content }
        requests.post(f"https://groupe5-python-mines.fr/channels/{id_channel}/messages/post",json = message)

class RemoteStorage: 
    def get_users(self)-> list[User]:
        liste = []
        response = requests.get("https://groupe5-python-mines.fr/users")
        for dico in response.json():
            liste.append(User(dico['name'],dico['id']))
        return liste
    
    def create_user(self,name):
        user = {'name' : name}
        requests.post("https://groupe5-python-mines.fr/users/create",json = user)

    def get_channel(self)-> list[User]:
        liste = []
        response = requests.get("https://groupe5-python-mines.fr/channels")
        for dico in response.json():
            members = requests.get(f"https://groupe5-python-mines.fr/channels/{dico['id']}/members").json()
            for dico_members in members:
                liste.append(Channel(dico['name'],dico['id'],dico_members['id'] ))
        return liste
    def create_channel(self,name, members):
        channel = {'name' : name }
        requests.post("https://groupe5-python-mines.fr/channels/create",json = channel)
    
    def add_user_channel(self,id_user,id_channel):
        requests.post(f"https://groupe5-python-mines.fr/channels/{id_channel}/join", )

    
    def get_message(self)-> list[User]:
        liste = []
        response = requests.get("https://groupe5-python-mines.fr/messages")
        for dico in response.json():
            liste.append(User(dico['name'],dico['id'], dico['member_ids']))
        return liste
    def create_message(self,name, members):
        channel = {'name' : name, 'member_ids' : members }
        requests.post("https://groupe5-python-mines.fr/channels/create",json = channel)



   
storage = RemoteStorage()
#storage.create_user('Valentin')   
#storage.create_channel('Amis',[1,2])
server = { 'users':[], 'channels' : [], 'messages' : []}
print(storage.get_channel_message(10))
#storage.create_message(10,'Bonjour Léonard', 8)

#print(storage.get_channel())
#print(storage.get_message())
storage.add_user_channel(4,2)
def print_logo():
    try:
        from pyfiglet import figlet_format
        banner = figlet_format("Messenger", font="slant")
    except Exception:
        banner = "== Messenger =="
    width = shutil.get_terminal_size((80, 20)).columns
    for line in banner.splitlines():
        print("\033[1;34m" + line.center(width) + "\033[0m")
    stats = f"Utilisateurs : {len(server['users'])}  |  Canaux : {len(server['channels'])}"
    print(stats.center(width) + "\n")
    print('=== Bienvenue dans le service de messagerie ==='.center(width))

with open("server.json", "r", encoding = "utf-8") as f: #Lecture du fichier uniquement 
    server1 = json.load(f)
for user in server1['users']: #conversion du server json en un server local utilisant les classes
    server['users'].append(User(user['name'],user['id'])) 
for group in server1['channels']:
    server['channels'].append(Channel(group['name'], group['id'], group['member_ids']))
for message in server1['messages']:
    server['messages'].append(Message(message['channel'],message['id'],message['content'], message['reception_date'], message['sender_id']))
#with open(RemoteStorage.get_users(), "r", encoding = "utf-8") as f: #Lecture du fichier uniquement 
    #web1 = json.load(f)
#print(web1)
def save_server(): #sauvegarde du server
     new_server = { 'users':[], 'channels' : [], 'messages' : []} #conversion inverse afin de changer les classes locales en des dictionnaires
     for user in server['users']:
         new_server['users'].append({'id' : user.id, 'name' : user.name})
     for channel in server['channels']:
         new_server['channels'].append({'id' : channel.idg, 'name' : channel.name, 'member_ids' : channel.members})
     for message in server['messages']:
         new_server['messages'].append({'id' : message.id, 
                                        'reception_date' : message.time, 
                                        'sender_id' : message.sender, 
                                        'channel' : message.channel,
                                        'content' : message.content})
     with open("server.json","w", encoding = "utf-8") as f: #écriture du fichier --> modification 
          json.dump(new_server, f, ensure_ascii=False, indent=2)

def indice(nom : str): #convertit un nom d'utilisateur en indice utilisateur 
    for user in server['users']:
        if user.name==nom:
            return user.id

def indice_vers_nom(indice : int):
    for user in server['users']:
        if user.id == indice:
            return user.name
def indice_g(groupe):#convertit un nom de groupe en indice de groupe 
    for group in server['channels']:
        if group.name == groupe:
            return groupe.idg

liste_id = [user.id for user in server['users']]

liste_idg = [group.idg for group in server['channels']]

liste_idm = [message.id for message in server['messages']]

liste = [user.name for user in server['users']]
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generer_id(L : list[int]): #génère un identifiant user
     return max(L)+1

def redirection(): #redirige vers le menu principal
    print('Redirections possibles : \nAffichage utilisateur : Au\n  \nAffichage messages groupe : Amg\n  \nAjouter un utilisateur : Aju\n  \nAjouter un groupe : Ajg\n \nAjouter plusieurs utilisateurs : Ajus\n  \nRetour menu principal : RM\n \nEcriture message : em')
    choix = input('Choix : ')
    if choix == 'Au':
        affiche_utilisateurs()
    elif choix == 'Amg':
        afficher_messages_groupes()
    elif choix == 'Aju':
        ajout_utilisateur()
    elif choix == 'Ajg':
        ajout_groupe()
    elif choix == 'Ajus':
         ajout_plusieurs_utilisateurs()
    elif choix =='em':
         ecriture_message()
    else:
        retour_menu()

def affiche_utilisateurs(): #affichage de tous les utilisateurs de la classe User
    #clear_screen()
    for user in storage.get_users():
        print(user.name)
    
def afficher_messages_groupes(): #affichage des messages d'un groupe sélectionné
   # clear_screen()
    for group in server['channels']:
            print(group.name)
    name_g = input ('Choisissez un groupe : ')
    number = indice_g(name_g)
    if number not in liste_idg:
        print ('Ce groupe nexiste pas')
    else:
        for message in server['messages']:
            if message.channel == number :
                print(message.content)
                break
            
def ajout_utilisateur():
 #  clear_screen()
    nom = input( 'Name : ')
    if nom in liste:
         print(f'utilisateur : {nom} est déja dans le serveur')
         redirection()
    id = generer_id(liste_id)
    user = User(nom, id)
    server['users'].append(user)
    save_server()
    liste_id.append(id)
    
def ajout_plusieurs_utilisateurs():
  #   clear_screen()
     liste_noms = input('Names : ').split(',')
     liste_noms_corr = [ user.strip() for user in liste_noms]
     for nom in liste_noms_corr : 
            id = generer_id(liste_id)
            user = User(nom,id)
            server['users'].append(user)
            liste_id.append(id)
            save_server()
     
def continuer_messagerie(groupe, user):
    choixd = input('Voulez-vous continuer à discuter ? (Oui/Non) :')
    print(choixd)
    if choixd == 'Oui':
        for message in server['messages']:
            if message.channel == groupe:
                print(colored(message.time, '1;36'), colored(indice_vers_nom(message.sender), '1;33')) #foncion couleur générée par l'IA, c'est uniquement pour l'esthétique
                print('')
                print(message.content)
                print('')
                print('')
        message = input('message :')
        #server['messages'].append()
        idm = generer_id(liste_idm)
        new_messagerie = Message(groupe, idm, message,str(datetime.now().strftime("%d/%m/%Y %H:%M")),indice(user))
        server['messages'].append(new_messagerie)
        continuer_messagerie(groupe,user)
    else:
        redirection()

def ajout_groupe_et_messagerie_privés():
   # clear_screen()
    nom1 = input ('Votre prénom : ') 
    nom2 = input( 'Personne avec qui vous voulez parler : ')
    N_ut = []
    if nom2 not in liste:
        N_ut.append(nom2)
    if len(N_ut) == 1:
        print(f'{N_ut} ne fait pas parti des utilisateurs, vous ne pouvez pas discuter avec lui/elle')
        redirection()
    nL = [indice(nom2), indice(nom1)]
    cpt =0
    for group in server['channels']:
        if group.members == nL or group.members == [indice(nom1),indice(nom2)]:
            cpt+=1
            id_pour_mess = group.idg
    if cpt ==0 : #si le groupe n'existe pas, on le crée
        id_group = generer_id(liste_idg) 
        idm = generer_id(liste_idm)
        group_name = input( 'Nom du groupe : ')
        messages = input('message : ')
        new_group = Channel(group_name,id_group,nL)
        new_messagerie = Message(id_group, idm, [],str(datetime.now().strftime("%d/%m/%Y %H:%M")),indice(nom1))
        server['messages'].append(new_messagerie)
        server['channels'].append(new_group)
        continuer_messagerie(id_group,nom1)
    else :
        idm = generer_id(liste_idm)
        messages = input('message : ')
        new_messagerie = Message(id_pour_mess, idm, messages,str(datetime.now().strftime("%d/%m/%Y %H:%M")),indice(nom1))
        server['messages'].append(new_messagerie)
        continuer_messagerie(id_pour_mess,nom1)
    save_server()
    
def ajout_groupe():
    #clear_screen()
    group_name = input( 'Name : ')
    id_group = generer_id(liste_idg)
    utilisateurs_group = input( 'Liste : ').split(',')
    user_corr = [ user.strip() for user in utilisateurs_group]
    N_ut = []
    for user in user_corr:
         if user not in liste:
              N_ut.append(user)
    if len(N_ut) == 1:
         print(f'{N_ut} ne fait pas parti des utilisateurs, il faut l ajouter :')
         ajout_utilisateur()
         ajout_groupe()
    elif len(N_ut) > 1:
         print(f'{N_ut} ne font pas parti des utilisateurs, il faut les ajouter :')
         ajout_plusieurs_utilisateurs() 
         ajout_groupe()        
    nL = []
    for x in user_corr:
        nL.append(indice(x))
    new_group = Channel(group_name,id_group,nL)
    server['channels'].append(new_group)
    save_server()  

def ecriture_message():
    #clear_screen()
    privé = input('Souhaitez vous parler en privé à un autre utilisateur (Oui/Non) ? :')
    if privé == 'Non':
        fuser_name = input('Votre prénom : ')
        print('Groupe(s) disponibles :')
        for group in server['channels']:
            if indice(fuser_name) in group.members:
                print(group.name)
        group_name = input('Quel est le groupe choisi ? :')
        indice_groupe = indice_g(group_name)
        idmes = generer_id(liste_idm)
        message = input('Discussion ouverte :' )
        server['messages'].append(Message(indice_groupe,idmes, message,str(datetime.now().strftime("%d/%m/%Y %H:%M")),indice(fuser_name)))
        continuer_messagerie(indice_groupe,fuser_name)
    else :
        ajout_groupe_et_messagerie_privés()

    save_server() 
    
def retour_menu():
    choix()

def choix():
    print_logo()
    print('Sortie du service : S \n \nAffichage utilisateurs : u\n \nAffichage messages groupe : g\n \nAjout utilisateur : au\n \nAjout Groupe : ag\n \nAjout plusieurs utilisateurs : apu\n \nEcrire un message : em\n \n')
    choice = input('Sélectionnez une option : ')
    if choice == 'u':
        affiche_utilisateurs()
        Bol = input('Voulez-vous continuer ? :')
        if Bol == 'Oui':
            redirection()
        
    elif choice == 'S':
        print('Sortie du service')
    

    elif choice == 'g':
        afficher_messages_groupes()
        Bol = input('Voulez-vous continuer ? :')
        if Bol == 'Oui':
            redirection()
        
    elif choice == 'au':
        ajout_utilisateur()
        Bol = input('Voulez-vous continuer ? :')
        if Bol == 'Oui':
            redirection()

    elif choice == 'apu':
         ajout_plusieurs_utilisateurs() 
         Bol = input('Voulez-vous continuer ? :')
         if Bol == 'Oui':
            redirection()  
        
    elif choice == 'ag':
        ajout_groupe()
        Bol = input('Voulez-vous continuer ? :')
        if Bol == 'Oui':
            redirection()

    elif choice == 'em':
        ecriture_message()
        Bol = input('Voulez-vous continuer ? :')
        if Bol == 'Oui':
            redirection()  

    else:
        print('Commande inconnue : ', choice)
        retour_menu()

#choix()
