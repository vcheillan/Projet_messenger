from datetime import datetime
import random 
import json



with open("server.json", "r", encoding = "utf-8") as f:
    server = json.load(f)

def save_server():
     with open("server.json","w", encoding = "utf-8") as f:
          json.dump(server, f, ensure_ascii=False, indent=2)

def indice(nom):
    for dico in server['users']:
        if dico['name']==nom:
            return dico['id']
liste_id = [dico['id'] for dico in server['users']]

liste_idg = [dico['id'] for dico in server['channels']]

liste = [dico['name'] for dico in server['users']]

def generer_id(L):
     return max(L)+1

def menu_principal(choice):
    MP = input('Do you want to go to the main menu ? ')
    if MP == 'Yes':
        choice = input('Select an option')

def redirection():
    print('Redirections possibles : \nAffichage utilisateur : Au,  \nAffichage messages groupe : Amg,  \nAjouter un utilisateur : Aju,  \nAjouter un groupe : Ajg, \nAjouter plusieurs utilisateurs : Ajus  \nRetour menu principal : RM')
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
    else:
        retour_menu()

def affiche_utilisateurs():
    for dico in server['users']:
            print(dico)
    Bol = input('Do you want to continue ? :')
    if Bol == 'Yes':
            redirection()

def afficher_messages_groupes():
    for dico in server['channels']:
            print(dico['name'])
    number = input ('Select a specific group : ')
    if number == 'NAN':
        print ('Okay bro')
    else:
        for dico in server['messages']:
            if dico['channel'] == int(number) :
                print(dico['content'])
                break
            else:
                print('This group doesnt exist')
    Bol = input('Do you want to continue ? :')
    if Bol == 'Yes':
            redirection()
    

def ajout_utilisateur():
    utilisateur = input( 'Name : ')
    if utilisateur in liste:
         print(f'utilisateur : {utilisateur} déja dans le serveur')
         redirection()
    id = generer_id(liste_id)
    server['users'].append({'id': id, 'name' : utilisateur})
    save_server()
    liste.append(utilisateur)
    liste_id.append(id)
    Bol = input('Do you want to continue ? :')
    if Bol == 'Yes':
            redirection()

def ajout_plusieurs_utilisateurs():
     liste_noms = input('Names : ').split(',')
     liste_noms_corr = [ user.strip() for user in liste_noms]
     for user in liste_noms_corr : 
            id = generer_id(liste_id)
            server['users'].append({'id': id, 'name' : user})
            liste.append(user)
            liste_id.append(id)
            save_server()
     Bol = input('Do you want to continue ? :')
     if Bol == 'Yes':
            redirection()

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
         print(f'{N_ut} ne fait pas parti des utilisateurs')
         ajout_utilisateur()
    elif len(N_ut) > 1:
         print(f'{N_ut} ne font pas parti des utilisateurs')
         ajout_plusieurs_utilisateurs()         
    nL = []
    for x in user_corr:
        nL.append(indice(x))
    ng = {'id': id_group, 'name' : group_name, 'member_ids' : nL}  
    server['channels'].append(ng)
    save_server()  
    #Availables_idg.pop(id_group)
    print(ng)
    Bol = input('Do you want to continue ? :')
    if Bol == 'Yes':
            redirection()

def retour_menu():
    choix()

def choix():
    print('=== Messenger ===')
    print('Sortie du service : Leave  \nAffichage utilisateurs : u \nAffichage messages groupe : g \nAjout utilisateur : au \nAjout Groupe : ag \nAjout plusieurs utilisateurs : apu')
    choice = input('Select an option: ')
    if choice == 'x':
        print('Bye!')
        
        
    elif choice == 'u':
        affiche_utilisateurs()
        
       
    elif choice == 'g':
        afficher_messages_groupes()
        
        
    elif choice == 'au':
        ajout_utilisateur()

    elif choice == 'apu':
         ajout_plusieurs_utilisateurs()   
        
    elif choice == 'ag':
        ajout_groupe()
            
    else:
        print('Unknown option:', choice)

choix()
