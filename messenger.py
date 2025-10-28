from datetime import datetime
import random 
import json

server = {
    'users': [
        {'id': 41, 'name': 'Alice'},
        {'id': 23, 'name': 'Bob'}
    ],
    'channels': [
        {'id': 12, 'name': 'Town square', 'member_ids': [41, 23]}
    ],
    'messages': [
        {
            'id': 18,
            'reception_date': datetime.now(),
            'sender_id': 41,
            'channel': 12,
            'content': 'Hi 👋'
        }
    ]
}
#my_server = json.loads(server)
def indice(nom):
    for dico in server['users']:
        if dico['name']==nom:
            return dico['id']
liste_id = [dico['id'] for dico in server['users']]
Availables_id = [ i for i in range(1000) if i not in liste_id]
liste_idg = [dico['id'] for dico in server['channels']]
Availables_idg = [ i for i in range(1000) if i not in liste_id]
def menu_principal(choice):
    MP = input('Do you want to go to the main menu ? ')
    if MP == 'Yes':
        choice = input('Select an option')

def redirection():
    print('Redirections possibles : Affichage utilisateur : Au, Affichage messages groupe : Amg, Ajouter un utilisateur : Aju, Ajouter un groupe : Ajg, Retour menu principal : RM')
    choix = input('Choix : ')
    if choix == 'Au':
        affiche_utilisateurs()
    elif choix == 'Amg':
        afficher_messages_groupes()
    elif choix == 'Aju':
        ajout_utilisateur()
    elif choix == 'Ajg':
        ajout_groupe()
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
    id = random.choice(Availables_id)
    server['users'].append({'id': id, 'name' : utilisateur})
    Availables_id.pop(id)
    print(server['users'])
    Bol = input('Do you want to continue ? :')
    if Bol == 'Yes':
            redirection()

def ajout_groupe():
    group_name = input( 'Name : ')
    id_group = random.choice(Availables_idg)
    id_utilisateurs_group = input( 'Liste : ').split(',')
    nL = []
    for x in id_utilisateurs_group:
        nL.append(indice(x))    
    server['channels'].append({'id': id_group, 'name' : group_name, 'members_ids' : nL})
    Availables_idg.pop(id_group)
    print(server['channels'])
    Bol = input('Do you want to continue ? :')
    if Bol == 'Yes':
            redirection()

def retour_menu():
    choix()

def choix():
    print('=== Messenger ===')
    print('x. Leave. u. g. au. ag.')
    choice = input('Select an option: ')
    if choice == 'x':
        print('Bye!')
        
        
    elif choice == 'u':
        affiche_utilisateurs()
        
       
    elif choice == 'g':
        afficher_messages_groupes()
        
        
    elif choice == 'au':
        ajout_utilisateur()
        
        
    elif choice == 'ag':
        ajout_groupe()
            
    else:
        print('Unknown option:', choice)

choix()
