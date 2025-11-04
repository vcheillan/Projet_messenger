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

def indice_g(groupe):
    for dico in server['channels']:
        if dico['name']==groupe:
            return dico['id']

liste_id = [dico['id'] for dico in server['users']]

liste_idg = [dico['id'] for dico in server['channels']]

liste = [dico['name'] for dico in server['users']]

def generer_id(L):
     return max(L)+1

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
         print(f'utilisateur : {utilisateur} déja dans le serveur')
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
            
    else:
        print('Unknown option:', choice)

choix()
