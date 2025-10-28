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
liste_id = [dico['id'] for dico in server['users']]
Availables_id = [ i for i in range(1000) if i not in liste_id]
liste_idg = [dico['id'] for dico in server['channels']]
Availables_idg = [ i for i in range(1000) if i not in liste_id]
def menu_principal(choice):
    MP = input('Do you want to go to the main menu ? ')
    if MP == 'Yes':
        choice = input('Select an option')
    
def choix():
    print('=== Messenger ===')
    print('x. Leave. u. g. au. ag.')
    choice = input('Select an option: ')
    if choice == 'x':
        print('Bye!')
        Bol = input('Do you want to continue ? :')
        if Bol == 'Yes':
           choix()
        
        #menu_principal(choice)
    elif choice == 'u':
        for dico in server['users']:
            print(dico)
        Bol = input('Do you want to continue ? :')
        if Bol == 'Yes':
           choix()
        
        # menu_principal(choice)
            
    elif choice == 'g':
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
           choix()
        
    elif choice == 'au':
        utilisateur = input( 'Name : ')
        id = random.choice(Availables_id)
        server['users'].append({'id': id, 'name' : utilisateur})
        Availables_id.pop(id)
        print(server['users'])
        Bol = input('Do you want to continue ? :')
        if Bol == 'Yes':
           choix()
        
    elif choice == 'ag':
        group_name = input( 'Name : ')
        id_group = random.choice(Availables_idg)
        id_utilisateurs_group = input( 'Liste : ')
        server['channels'].append({'id': id_group, 'name' : group_name, 'members_ids' : id_utilisateurs_group})
        Availables_idg.pop(id)
        print(server['channels'])
        Bol = input('Do you want to continue ? :')
        if Bol == 'Yes':
           choix()
            
    else:
        print('Unknown option:', choice)

choix()
