from datetime import datetime
import random 
import json

class User:
    def __init__(self, name: str, id: str): 
        self.name = name
        self.id = id



class Channel:
    def __init__(self, name: str, idg: int,members : list): 
        self.name = name
        self.idg = idg
        self.members = members



class Message:
    def __init__(self, channel: int, id: int,content : list[str], time : str, sender : int): 
        self.channel = channel
        self.id = id
        self.content = content
        self.time = time
        self.sender = sender


server = { 'users':[], 'channels' : [], 'messages' : []}

with open("server.json", "r", encoding = "utf-8") as f: #Lecture du fichier uniquement 
    server1 = json.load(f)
for user in server1['users']:
    server['users'].append(User(user['name'],user['id']))
for group in server1['channels']:
    server['channels'].append(Channel(group['name'], group['id'], group['member_ids']))
for message in server1['messages']:
    server['messages'].append(Message(message['channel'],message['id'],message['content'], message['reception_date'], message['sender_id']))

def save_server():
     new_server = { 'users':[], 'channels' : [], 'messages' : []}
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

def indice(nom):
    for user in server['users']:
        if user.name==nom:
            return user.id

def indice_g(groupe):
    for group in server['channels']:
        if group.name == groupe:
            return groupe.idg

liste_id = [user.id for user in server['users']]

liste_idg = [group.idg for group in server['channels']]

liste_idm = [message.id for message in server['messages']]

liste = [user.name for user in server['users']]

def generer_id(L : list[int]):
     return max(L)+1

def redirection():
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

def affiche_utilisateurs():
    for user in server['users']:
        print(user.name)
    
def afficher_messages_groupes():
    for group in server['channels']:
            print(group.name)
    name_g = input ('Select a specific group : ')
    number = indice_g(name_g)
    if number not in liste_idg:
        print ('Ce groupe nexiste pas')
    else:
        for message in server['messages']:
            if message.channel == number :
                print(message.content)
                break
            
def ajout_utilisateur():
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
     liste_noms = input('Names : ').split(',')
     liste_noms_corr = [ user.strip() for user in liste_noms]
     for nom in liste_noms_corr : 
            id = generer_id(liste_id)
            user = User(nom,id)
            server['users'].append(user)
            liste_id.append(id)
            save_server()
     
def continuer_messagerie(groupe, user):
    choixd = input('Voulez-vous continuer à discuter ? (Oui/Non)').split()
    if choixd == 'Oui':
        for dico_groupe in server['messages']:
            if dico_groupe['channel'] == groupe:
                print(dico_groupe['content'])
        message = input('Discussion ouverte')
        #server['messages'].append()
        idm = generer_id(liste_idm)
        new_messagerie = {'id' : idm, 
                          'reception_date' : str(datetime.now().strftime("%d/%m/%Y %H:%M")), 
                          'sender_id':indice(user), 
                          'channel':groupe, 
                          'content' : message }
        server['messages'].append(new_messagerie)
        continuer_messagerie()
    else:
        redirection()

def ajout_groupe_et_messagerie_privés():
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
    if cpt ==0 : 
        id_group = generer_id(liste_idg) 
        idm = generer_id(liste_idm)
        group_name = input( 'Nom du groupe : ')
        messages = input('Discussion ouverte')
        new_group = Channel(group_name,id_group,nL)
        new_messagerie = Message(id_group, idm, [],str(datetime.now().strftime("%d/%m/%Y %H:%M")),indice(nom1))
        server['messages'].append(new_messagerie)
        server['channels'].append(new_group)
        continuer_messagerie(id_group,nom1)
    else :
        idm = generer_id(liste_idm)
        messages = input('Discussion ouverte')
        new_messagerie = Message(id_pour_mess, idm, messages,str(datetime.now().strftime("%d/%m/%Y %H:%M")),indice(nom1))
        server['messages'].append(new_messagerie)
        continuer_messagerie(id_pour_mess,nom1)
    save_server()
    
def ajout_groupe():
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
    server['channel'].append(new_group)
    save_server()  

def ecriture_message():
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
    print('=== Messenger ===')
    print('Sortie du service : Leave \n \nAffichage utilisateurs : u\n \nAffichage messages groupe : g\n \nAjout utilisateur : au\n \nAjout Groupe : ag\n \nAjout plusieurs utilisateurs : apu\n \nEcrire un message : em\n \n')
    choice = input('Select an option: ')
    if choice == 'x':
        print('Bye!')
    elif choice == 'u':
        affiche_utilisateurs()
        Bol = input('Voulez-vous continuer ? :')
        if Bol == 'Oui':
            redirection()
        
       
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
        print('Unknown option:', choice)

choix()
