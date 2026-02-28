from datetime import datetime
import os
import shutil
from remote_storage import RemoteStorage
from local_storage import LocalStorage
import argparse

# Petite aide pour colorer le texte dans le terminal (codes ANSI)
def colored(text: str, color_code: str) -> str:
    return f"\033[{color_code}m{text}\033[0m"

#def Local_ou_Remote():
    choix  = input('Bonjour, souhaitez-vous travailler en local (L) ou en Remote (R) ? :')
    if choix == 'L':
        storage = LocalStorage("server.json")
    else : 
        storage = RemoteStorage()

    return storage
#storage = Local_ou_Remote()
#print(storage.get_channel())
#storage.create_user('Valentin')   
#storage.create_channel('Amis',[1,2])
server = { 'users':[], 'channels' : [], 'messages' : []}
#print(storage.get_channel_message(10))
#storage.create_message(10,'Bonjour Léonard', 8)
parser = argparse.ArgumentParser(
                    prog='Messenger',
                    description='Description du service de messagerie',
                    epilog='Vous êtes paumés et vous ne savez pas comment utiliser le service de messsagerie ?\n Vous êtes tombés au bon endroit !\n Le service vous permet d utiliser plusieurs focntions, en commençant par afficher des utilisateurs, en ajouter. Vous pouvez aussi parler à des utilsateurs en groupe ou en message privé')


parser.add_argument('--remote', help = 'Nom URL')
parser.add_argument('--local', help = 'Nom du fichier')
args = parser.parse_args()

if args.remote:
    storage = RemoteStorage(args.remote)

elif args.local:
    storage = LocalStorage(args.local)

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
    print(colored('═' * width, '1;34'))
    print('=== Bienvenue dans le service de messagerie ==='.center(width))
    print(colored('═' * width, '1;34') + '\n')

def indice(nom : str): #convertit un nom d'utilisateur en indice utilisateur 
    for user in storage.get_users():
        if user.name==nom:
            return user.id

def indice_vers_nom(indice : int):
    for user in storage.get_users():
        if user.id == indice:
            return user.name
def indice_g(name):#convertit un nom de groupe en indice de groupe 
    for group in storage.get_channel():
        if group.name == name:
            return group.idg
def indice_g_vers_nom(id_channel):
    for group in storage.get_channel():
        if group.idg == id_channel:
            return group.name

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
            print(f"  {colored(f'[ID: {user.id}]', '1;33')} {colored(user.name, '1;32')}")
    print('='*50)
    redirection()
    
def afficher_messages_groupes(): #affichage des messages d'un groupe sélectionné
   # clear_screen()
    print('\n' + colored('📂 GROUPES DISPONIBLES', '1;36'))
    print('='*50)
    channels = storage.get_channel()
    if not channels:
        print(colored('Aucun groupe disponible', '1;31'))
        redirection()
        return
    for group in channels:
        print(f"  {colored(f'[ID: {group.idg}]', '1;33')} {colored(group.name, '1;32')}")
    print('='*50)
    id_g = input(colored('Choisissez un groupe (son identifiant): ', '1;33'))
    messages = storage.get_channel_message(int(id_g))
    print('\n' + colored(f'💬 Groupe : {indice_g_vers_nom(int(id_g))}', '1;36'))
    print('='*50)
    if not messages:
        print(colored('Aucun message dans ce groupe', '1;31'))
    else:
        for message in messages :
            print(f"\n{colored(message.time, '1;36')} | {colored(indice_vers_nom(message.sender), '1;33')}")
            print(f"{message.content}")
    print('\n' + '='*50)
    redirection()

            
def ajout_utilisateur():
 #  clear_screen()
    print('\n' + colored('➕ AJOUTER UN UTILISATEUR', '1;36'))
    print('='*50)
    nom = input(colored('Pseudo : ', '1;33'))
    liste = [user.name for user in storage.get_users()]
    if nom in liste:
        print(colored(f'❌ Erreur : L\'utilisateur {nom} existe déjà !', '1;31'))
        redirection()
    else:
        storage.create_user(nom)
        print(colored(f'✓ Utilisateur {nom} ajouté avec succès !', '1;32'))
    print('='*50)
    redirection()
    #save_server()
    #liste_id.append(id)
    
def ajout_plusieurs_utilisateurs():
  #   clear_screen()
    print('\n' + colored('➕ AJOUTER PLUSIEURS UTILISATEURS', '1;36'))
    print('='*50)
    liste_noms = input(colored('Pseudos (séparés par des virgules) : ', '1;33')).split(',')
    liste_noms_corr = [ user.strip() for user in liste_noms]
    for nom in liste_noms_corr :
        if nom:  # Ignorer les chaînes vides
            storage.create_user(nom)
            print(colored(f'  ✓ {nom}', '1;32'))
    print('='*50)
    redirection()
     
def continuer_messagerie(groupe, user_name):
    for message in storage.get_channel_message(groupe):
        print(f"\n{colored(message.time, '1;36')} | {colored(indice_vers_nom(message.sender), '1;33')}")
        print(f"{message.content}")
    print('\n' + '='*50)
    choixd = input(colored('Continuer la discussion ? (Oui/Non) : ', '1;33')).strip()
    if choixd.lower() == 'oui':
        message = input(colored('Votre message : ', '1;33'))
        if message.strip():
            storage.create_message(groupe, message, indice(user_name))
            continuer_messagerie(groupe, user_name)
        else:
            continuer_messagerie(groupe, user_name)
    else:
        redirection()

def ajout_groupe_et_messagerie_privés():
   # clear_screen()
    print('\n' + colored('💌 MESSAGERIE PRIVÉE', '1;36'))
    print('='*50)
    nom1 = input(colored('Votre prénom : ', '1;33')) 
    nom2 = input(colored('Personne avec qui vous souhaitez discuter : ', '1;33'))
    N_ut = []
    liste = [user.name for user in storage.get_users()]
    if nom2 not in liste:
        N_ut.append(nom2)
    if len(N_ut) == 1:
        print(colored(f'❌ Erreur : {nom2} n\'existe pas dans les utilisateurs', '1;31'))
        print('='*50)
        redirection()
        return
    nL = [indice(nom2), indice(nom1)]
    cpt = 0
    id_pour_mess = None
    for group in storage.get_channel():
        if group.members == nL or group.members == [indice(nom1),indice(nom2)]:
            cpt += 1
            id_pour_mess = group.idg
    if cpt == 0: #si le groupe n'existe pas, on le crée
        group_name = input(colored('Nom de la discussion : ', '1;33'))
        messages = input(colored('Votre message : ', '1;33'))
        id_channel = storage.create_channel(group_name)
        storage.create_message(id_channel, messages, indice(nom1))
        print(colored(f'✓ Discussion {group_name} créée !', '1;32'))
        print('='*50)
        continuer_messagerie(id_channel, nom1)
    else:
        messages = input(colored('Votre message : ', '1;33'))
        storage.create_message(id_pour_mess, messages, indice(nom1))
        continuer_messagerie(id_pour_mess, nom1)
    
def ajout_groupe():
    #clear_screen()
    print('\n' + colored('📂 CRÉER UN GROUPE', '1;36'))
    print('='*50)
    group_name = input(colored('Nom du groupe : ', '1;33'))
    utilisateurs_group = input(colored('Utilisateurs, au minimum 3 (séparés par des virgules) : ', '1;33')).split(',')
    user_corr = [ user.strip() for user in utilisateurs_group if user.strip()]
    N_ut = []
    liste = [user.name for user in storage.get_users()]
    for user in user_corr:
         if user not in liste:
              N_ut.append(user)
    if len(N_ut) == 1:
         print(colored(f'❌ Erreur : {N_ut[0]} n\'existe pas', '1;31'))
         print('='*50)
         ajout_utilisateur()
         ajout_groupe()
    elif len(N_ut) > 1:
         print(colored(f'❌ Erreur : {N_ut} n\'existent pas', '1;31'))
         print('='*50)
         ajout_plusieurs_utilisateurs() 
         ajout_groupe()
    else:
        id_channel = storage.create_channel(group_name)
        for name in user_corr:
            storage.add_user_channel(indice(name), id_channel)
        print(colored(f'✓ Groupe {group_name} créé avec succès !', '1;32'))
        print('='*50)
        redirection()
    #server['channels'].append(new_group)
    #save_server()  

def ecriture_message():
    #clear_screen()
    print('\n' + colored('✉️  MODE DE DISCUSSION', '1;36'))
    print('='*50)
    privé = input(colored('Privé ou Groupe ? (Privé/Groupe) : ', '1;33')).strip().lower()
    if privé == 'groupe':
        fuser_name = input(colored('Votre prénom : ', '1;33'))
        print(colored('\nVos groupes :', '1;36'))
        L = []
        for group in storage.get_channel():
            if len(group.members) >= 3:
                for user in group.members:
                    if indice(fuser_name) == user:
                        L.append(user)
                        print(f"  {colored(f'[ID: {group.idg}]', '1;33')} {colored(group.name, '1;32')}")
        if len(L) == 0:
            print(colored("  Aucun groupe trouvé", '1;31'))
            ajout_groupe()
            return
        group_name = input(colored('Nom du groupe : ', '1;33'))
        indice_groupe = indice_g(group_name)
        message = input(colored('Votre message : ', '1;33'))
        storage.create_message(indice_groupe, message, indice(fuser_name))
        continuer_messagerie(indice_groupe, fuser_name)
    else:
        ajout_groupe_et_messagerie_privés()

    #save_server() 
    
def retour_menu():
    choix()

def choix():
    print_logo()
    print('\n' + '='*50)
    print(colored('MENU PRINCIPAL', '1;36'))
    print('='*50)
    print(colored('u  ', '1;32') + '→ Afficher les utilisateurs')
    print(colored('g  ', '1;32') + '→ Afficher les messages de groupe')
    print(colored('au ', '1;32') + '→ Ajouter un utilisateur')
    print(colored('ag ', '1;32') + '→ Créer un groupe')
    print(colored('apu', '1;32') + ' → Ajouter plusieurs utilisateurs')
    print(colored('em ', '1;32') + '→ Écrire un message')
    print(colored('S  ', '1;31') + '→ Quitter le service')
    print('='*50)
    choice = input(colored('Sélectionnez une option : ', '1;33')).strip().lower()
    if choice == 'u':
        affiche_utilisateurs()
    elif choice == 's':
        print(colored('\n👋 Merci d\'avoir utilisé Messenger ! À bientôt !', '1;32'))
        return
    elif choice == 'g':
        afficher_messages_groupes()
    elif choice == 'au':
        ajout_utilisateur()
    elif choice == 'apu':
        ajout_plusieurs_utilisateurs()
    elif choice == 'ag':
        ajout_groupe()
    elif choice == 'em':
        ecriture_message()
    else:
        print(colored(f'❌ Commande inconnue : {choice}', '1;31'))
        retour_menu()

choix()
