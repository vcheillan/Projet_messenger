from datetime import datetime
import random 
import json
import os
import shutil
import requests
from model import User
from model import Channel
from model import Message
from local_storage import LocalStorage
# Petite aide pour colorer le texte dans le terminal (codes ANSI)
def colored(text: str, color_code: str) -> str:
    return f"\033[{color_code}m{text}\033[0m"
 
storage = LocalStorage()
#print(storage.get_channel())
#storage.create_user('Valentin')   
#storage.create_channel('Amis',[1,2])
server = storage.load_server()
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
    users_count = len(storage.get_users())
    channels_count = len(storage.get_channel())
    stats = f"👥 Utilisateurs : {users_count}  |  💬 Canaux : {channels_count}"
    print(stats.center(width) + "\n")
    print(colored('\u2550' * width, '1;34'))
    print('=== Bienvenue dans le service de messagerie ==='.center(width))
    print(colored('\u2550' * width, '1;34') + '\n')


def indice(nom : str): #convertit un nom d'utilisateur en indice utilisateur 
    for user in storage.get_users():
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

liste_id = [user.id for user in storage.get_users()]

liste_idg = [group.idg for group in storage.get_channel()]

liste_idm = [message.id for message in storage.get_message()]

liste = [user.name for user in storage.get_users()]
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generer_id(L : list[int]): #génère un identifiant user
     return max(L)+1

def redirection(): #redirige vers le menu principal
    print('\n' + '='*50)
    print(colored('MENU DE REDIRECTION', '1;36'))
    print('='*50)
    print(colored('Au ', '1;32') + '→ Affichage utilisateurs')
    print(colored('Amg', '1;32') + ' → Affichage messages groupe')
    print(colored('Aju', '1;32') + ' → Ajouter un utilisateur')
    print(colored('Ajg', '1;32') + ' → Ajouter un groupe')
    print(colored('Ajus', '1;32') + '→ Ajouter plusieurs utilisateurs')
    print(colored('em ', '1;32') + '→ Écriture message')
    print(colored('RM ', '1;32') + '→ Retour au menu principal')
    print('='*50)
    choix = input(colored('Votre choix : ', '1;33'))
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
    print('\n' + colored('📋 LISTE DES UTILISATEURS', '1;36'))
    print('='*50)
    users = storage.get_users()
    if not users:
        print(colored('Aucun utilisateur enregistré', '1;31'))
    else:
        for user in users:
            print(f"  {colored(f'[{user.name}]', '1;32')}")
    print('='*50)
    
def afficher_messages_groupes(): #affichage des messages d'un groupe sélectionné
   # clear_screen()
    print('\n' + colored('📂 GROUPES DISPONIBLES', '1;36'))
    print('='*50)
    channels = storage.get_channel()
    if len(channels) ==0:
        print(colored('Aucun groupe disponible', '1;31'))
        redirection()
    for group in channels:
        print(f"  {colored(f'[ID: {group.idg}]', '1;33')} {colored(group.name, '1;32')}")
    print('='*50)
    name_g = input(colored('Choisissez un groupe (son identifiant): ', '1;33'))
    messages = storage.get_channel_message(name_g)
    print('\n' + colored(f'💬 Groupe : {name_g}', '1;36'))
    print('='*50)
    if len(messages) ==0:
        print(colored('Aucun message dans ce groupe', '1;31'))
    else:
        for message in messages :
            print(f"\n{colored(message.time, '1;36')} | {colored(str(message.sender), '1;33')}")
            print(f"{message.content}")
    print('\n' + '='*50)

            
def ajout_utilisateur():
 #  clear_screen()
    print('\n' + colored('➕ AJOUTER UN UTILISATEUR', '1;36'))
    print('='*50)
    nom = input(colored('Nom : ', '1;33'))
    if nom in liste:
        print(colored(f'❌ Erreur : L\'utilisateur {nom} existe déjà !', '1;31'))
        redirection()
    else:
        id = storage.create_user(nom)
        save_server()
        liste_id.append(id)
        print(colored(f'✓ Utilisateur {nom} ajouté avec succès !', '1;32'))
    print('='*50)
    redirection()
    
def ajout_plusieurs_utilisateurs():
  #   clear_screen()
    print('\n' + colored('➕ AJOUTER PLUSIEURS UTILISATEURS', '1;36'))
    print('='*50)
    liste_noms = input(colored('Noms (séparés par des virgules) : ', '1;33')).split(',')
    liste_noms_corr = [ user.strip() for user in liste_noms]
    for nom in liste_noms_corr :
        if nom:  # Ignorer les chaînes vides
            id = generer_id(liste_id)
            storage.create_user(nom)
            liste_id.append(id)
            save_server()
            print(colored(f'  ✓ {nom}', '1;32'))
    print('='*50)
    redirection()
     
def continuer_messagerie(groupe, user):
    choixd = input('Voulez-vous continuer à discuter ? (Oui/Non) :')
    print(choixd)
    if choixd == 'Oui':
        for message in storage.get_channel_message(groupe.idg):
            print(colored(message.time, '1;36'), colored(indice_vers_nom(message.sender), '1;33')) #foncion couleur générée par l'IA, c'est uniquement pour l'esthétique
            print('')
            print(message.content)
            print(''OO)
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
    save_server()
    
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
    save_server()  

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

choix()
