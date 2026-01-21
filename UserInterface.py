class UserInterface():
    def __init__(self, storage): #crétion de la classe User qui contient tous les élements du dico LocalStroage
        self.storage = storage

def affiche_utilisateurs(): #affichage de tous les utilisateurs de la classe User
    #clear_screen()
    for user in storage.get_users():
        print(user.id,' : ',user.name)
    redirection()
    
def afficher_messages_groupes(): #affichage des messages d'un groupe sélectionné
   # clear_screen()
    for group in self.storage.get_channel():
            print(group.idg, ' : ',group.name )
    id_g = input ('Choisissez un groupe (son identifiant): ')
    messages = storage.get_channel_message(int(id_g))
    print("=====\033[3m" + f'Groupe : {indice_g_vers_nom(int(id_g))}' + "\033[0m====")
    print('')
    for message in messages :
        print(colored(message.time, '1;36'), colored(indice_vers_nom(message.sender), '1;33')) #foncion couleur générée par l'IA, c'est uniquement pour l'esthétique
        print('')
        print(message.content)
        print('')

    