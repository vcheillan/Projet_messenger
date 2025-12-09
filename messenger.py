from datetime import datetime
import random 
import json

class User:
    def __init__(self, name: str, firstname: str): 
        self.name = name
        self.firstname = firstname

with open("server.json", "r", encoding = "utf-8") as f: #Lecture du fichier uniquement 
    server = json.load(f)

def save_server():
     with open("server.json","w", encoding = "utf-8") as f: #écriture du fichier --> modification 
          json.dump(server, f, ensure_ascii=False, indent=2)

def indice(nom):
    for dico in server['users']:
        if dico['name']==nom:
            return dico['id']

def indice_g(groupe):
    for dico in server['channels']:
        if dico['name']==groupe:
            return dico['id']

liste_id = [dico['id'] for dico in server['users']]

liste_idg = [dico['id'] for dico in server['channels']]

liste_idm = [dico['id'] for dico in server['messages']]

liste = [dico['name'] for dico in server['users']]

def generer_id(L):
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
    for dico in server['users']:
            print(dico)
    
def afficher_messages_groupes():
    for dico in server['channels']:
            print(dico['name'])
    name_g = input ('Select a specific group : ')
    number = indice_g(name_g)
    if number not in liste_idg:
        print ('Ce groupe nexiste pas')
    else:
        for dico in server['messages']:
            if dico['channel'] == number :
                print(dico['content'])
                break
            
def ajout_utilisateur():
    utilisateur = input( 'Name : ')
    if utilisateur in liste:
         print(f'utilisateur : {utilisateur} est déja dans le serveur')
         redirection()
    id = generer_id(liste_id)
    server['users'].append({'id': id, 'name' : utilisateur})
    save_server()
    liste.append(utilisateur)
    liste_id.append(id)
    
def ajout_plusieurs_utilisateurs():
     liste_noms = input('Names : ').split(',')
     liste_noms_corr = [ user.strip() for user in liste_noms]
     for user in liste_noms_corr : 
            id = generer_id(liste_id)
            server['users'].append({'id': id, 'name' : user})
            liste.append(user)
            liste_id.append(id)
            save_server()
     
def continuer_messagerie(groupe, user):
    choixd = input('Voulez-vous continuer à discuter ? (Oui/Non)')
    if choixd == 'Oui':
        for dico_groupe in server['messages']:
            if dico_groupe['channel'] == groupe:
                print(dico_groupe['content'])
        message = input('Discussion ouverte')
        server['messages'].append()
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
    first_user = input ('Votre prénom : ') 
    
    
    autre_utilisateur = input( 'Personne avec qui vous voulez parler : ')
    N_ut = []
    if autre_utilisateur not in liste:
        N_ut.append(autre_utilisateur)
    if len(N_ut) == 1:
        print(f'{N_ut} ne fait pas parti des utilisateurs, vous ne pouvez pas discuter avec lui/elle')
        redirection()
    nL = [indice(autre_utilisateur), indice(first_user)]
    cpt =0
    for dico in server['channels']:
        if dico['member_ids'] == nL or dico['member_ids'] == [indice(first_user),indice(autre_utilisateur)]:
            cpt+=1
            id_pour_mess = dico['id']
    if cpt ==0 :  
        ng = {'id': id_group, 'name' : group_name, 'member_ids' : nL }  
        server['channels'].append(ng)
        idm = generer_id(liste_idm)
        group_name = input( 'Nom du groupe : ')
        id_group = generer_id(liste_idg)
        messages = input('Discussion ouverte')
        new_messagerie = {'id' : idm, 
                          'reception_date' : str(datetime.now().strftime("%d/%m/%Y %H:%M")), 
                          'sender_id':indice(first_user), 
                          'channel':id_group, 
                          'content' : messages }
        server['messages'].append(new_messagerie)
        continuer_messagerie(id_group,first_user)
    else :
        idm = generer_id(liste_idm)
        messages = input('Discussion ouverte')
        new_messagerie = {'id' : idm, 
                          'reception_date' : str(datetime.now().strftime("%d/%m/%Y %H:%M")), 
                          'sender_id':indice(first_user), 
                          'channel':id_pour_mess, 
                          'content' : messages }
        server['messages'].append(new_messagerie)
        continuer_messagerie(id_pour_mess,first_user)

    
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
    ng = {'id': id_group, 'name' : group_name, 'member_ids' : nL}  
    server['channels'].append(ng)
    save_server()  
    #Availables_idg.pop(id_group)
    print(ng)

def ecriture_message():
    privé = input('Souhaitez vous parler en privé à un autre utilisateur (Oui/Non) ? :')
    if privé == 'Non':
        fuser_name = input('Votre prénom : ')
        print('Groupe(s) disponibles :')
        for group in server['channels']:
            if indice(fuser_name) in group['member_ids']:
                print(group['name'])
        group_name = input('Quel est le groupe choisi ? :')
        indice_groupe = indice_g(group_name)
        idmes = generer_id(liste_idm)
        message = input('Discussion ouverte :' )
        server['messages'].append({'id' : idmes, 
                                   'reception_date' : str(datetime.now().strftime("%d/%m/%Y %H:%M")), 
                                   'sender_id':indice(fuser_name), 
                                   'channel':indice_groupe, 
                                   'content' : message })
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
