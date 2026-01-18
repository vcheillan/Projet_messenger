from datetime import datetime
import random 
import json
import os
import shutil
import requests
from model import User
from model import Channel
from model import Message
from remote_storage import RemoteStorage
# Petite aide pour colorer le texte dans le terminal (codes ANSI)
def colored(text: str, color_code: str) -> str:
    return f"\033[{color_code}m{text}\033[0m"
 
storage = RemoteStorage()
#print(storage.get_channel())
#storage.create_user('Valentin')   
#storage.create_channel('Amis',[1,2])
server = { 'users':[], 'channels' : [], 'messages' : []}
#print(storage.get_channel_message(10))
#storage.create_message(10,'Bonjour Léonard', 8)

#print(storage.get_channel())
#print(storage.get_message())
#storage.add_user_channel(4,2)
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


def indice(nom : str): #convertit un nom d'utilisateur en indice utilisateur 
    for user in storage.get_users():
        if user.name==nom:
            return user.id

def indice_vers_nom(indice : int):
    for user in storage.get_users():
        if user.id == indice:
            return user.name
def indice_g(groupe):#convertit un nom de groupe en indice de groupe 
    for group in storage.get_channel():
        if group.name == groupe:
            return groupe.idg

liste_id = [user.id for user in storage.get_users()]

liste_idg = [group.idg for group in storage.get_channel()]

liste_idm = [message.id for message in storage.get_message()]

liste = [user.name for user in storage.get_users()]
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
    for group in storage.get_channel():
            print(group.name, group.idg)
    name_g = input ('Choisissez un groupe (son identifiant): ')
    messages = storage.get_channel_message(name_g)
    for message in messages :
        print(message.content)

            
def ajout_utilisateur():
 #  clear_screen()
    nom = input( 'Name : ')
    if nom in liste:
         print(f'utilisateur : {nom} est déja dans le serveur')
         redirection()
    id = storage.create_user(nom)
    #save_server()
    liste_id.append(id)
    
def ajout_plusieurs_utilisateurs():
  #   clear_screen()
     liste_noms = input('Names : ').split(',')
     liste_noms_corr = [ user.strip() for user in liste_noms]
     for nom in liste_noms_corr : 
            id = generer_id(liste_id)
            #user = User(nom,id)
            storage.create_user(nom)
            #server['users'].append(user)
            liste_id.append(id)
            #save_server()
     
def continuer_messagerie(groupe, user):
    choixd = input('Voulez-vous continuer à discuter ? (Oui/Non) :')
    print(choixd)
    if choixd == 'Oui':
        for message in storage.get_channel_message(groupe.idg):
            print(colored(message.time, '1;36'), colored(indice_vers_nom(message.sender), '1;33')) #foncion couleur générée par l'IA, c'est uniquement pour l'esthétique
            print('')
            print(message.content)
            print('')
            print('')
        message = input('message :')
        #server['messages'].append()
        storage.create_message(groupe.idg,message, user.id)
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
    for group in storage.get_channel():
        if group.members == nL or group.members == [indice(nom1),indice(nom2)]:
            cpt+=1
            id_pour_mess = group.idg
    if cpt ==0 : #si le groupe n'existe pas, on le crée
        #id_group = generer_id(liste_idg) 
        #idm = generer_id(liste_idm)
        group_name = input( 'Nom du groupe : ')
        messages = input('message : ')
        #new_group = Channel(group_name,id_group,nL)
        #new_messagerie = Message(id_group, idm, [],str(datetime.now().strftime("%d/%m/%Y %H:%M")),indice(nom1))
        id_channel = storage.create_channel(group_name)
        storage.create_message(id_channel, messages, indice(nom1))
        #server['messages'].append(new_messagerie)
        #server['channels'].append(new_group)
        continuer_messagerie(id_channel,nom1)
    else :
        #idm = generer_id(liste_idm)
        messages = input('message : ')
        #new_messagerie = Message(id_pour_mess, idm, messages,str(datetime.now().strftime("%d/%m/%Y %H:%M")),indice(nom1))
        storage.create_message(id_pour_mess,messages,indice(nom1))
        #server['messages'].append(new_messagerie)
        continuer_messagerie(id_pour_mess,nom1)
    #save_server()
    
def ajout_groupe():
    #clear_screen()
    group_name = input( 'Name : ')
    #id_group = generer_id(liste_idg)
    utilisateurs_group = input( 'Liste des utilisateurs : ').split(',')
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
    #new_group = Channel(group_name,id_group,nL)
    id_channel = storage.create_channel(group_name)
    for name in user_corr:
        storage.add_user_channel(indice(name),id_channel)
    #server['channels'].append(new_group)
    #save_server()  

def ecriture_message():
    #clear_screen()
    privé = input('Souhaitez vous parler en privé à un autre utilisateur (Oui/Non) ? :')
    if privé == 'Non':
        fuser_name = input('Votre prénom : ')
        print('Groupe(s) disponibles :')
        for group in storage.get_channel():
            for user in group.members:
                if fuser_name == user['name']:
                    print(group.idg,':' ,group.name)
        group_name = input('Quel est le groupe choisi ? :')
        indice_groupe = indice_g(group_name)
        #idmes = generer_id(liste_idm)
        message = input('Discussion ouverte :' )
        #server['messages'].append(Message(indice_groupe,idmes, message,str(datetime.now().strftime("%d/%m/%Y %H:%M")),indice(fuser_name)))
        storage.create_message(indice_groupe,message,indice(fuser_name))
        continuer_messagerie(group,fuser_name)
    else :
        ajout_groupe_et_messagerie_privés()

    #save_server() 
    
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

choix()
