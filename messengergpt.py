from datetime import datetime
import random
import json
import os
import shutil

# couleurs et helpers d'affichage (esthétique seulement)
RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[1;34m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"


def _term_width():
    return shutil.get_terminal_size((80, 20)).columns


def center_lines(text, color=""):
    w = _term_width()
    for line in str(text).splitlines():
        print((color + line.center(w) + RESET) if color else line.center(w))


def print_list(title, items, color=CYAN):
    center_lines(title, color=GREEN)
    for i, it in enumerate(items, 1):
        center_lines(f"{i}. {it}", color)


class User:
    def __init__(self, name: str, id: int):  # création de la classe User
        self.name = name
        self.id = id


class Channel:
    def __init__(self, name: str, idg: int, members: list):  # création Channel
        self.name = name
        self.idg = idg
        self.members = members


class Message:
    def __init__(self, channel: int, id: int, content, time: str, sender: int):  # création Message
        self.channel = channel
        self.id = id
        self.content = content
        self.time = time
        self.sender = sender


server = {"users": [], "channels": [], "messages": []}


def print_logo():
    try:
        from pyfiglet import figlet_format

        banner = figlet_format("Messenger", font="slant")
    except Exception:
        banner = "== Messenger =="
    width = _term_width()
    for line in banner.splitlines():
        print("\033[1;34m" + line.center(width) + "\033[0m")
    stats = f"Utilisateurs : {len(server['users'])}  |  Canaux : {len(server['channels'])}"
    print(stats.center(width) + "\n")
    print("=== Bienvenue dans le service de messagerie ===".center(width))


# chargement du server.json en mémoire
with open("server.json", "r", encoding="utf-8") as f:  # Lecture du fichier uniquement
    server1 = json.load(f)

for user in server1.get("users", []):  # conversion json -> objects locaux
    server["users"].append(User(user["name"], user["id"]))
for group in server1.get("channels", []):
    server["channels"].append(Channel(group["name"], group["id"], group.get("member_ids", [])))
for message in server1.get("messages", []):
    server["messages"].append(
        Message(message.get("channel"), message.get("id"), message.get("content"), message.get("reception_date"), message.get("sender_id"))
    )


def save_server():  # sauvegarde du server
    new_server = {"users": [], "channels": [], "messages": []}  # conversion inverse
    for user in server["users"]:
        new_server["users"].append({"id": user.id, "name": user.name})
    for channel in server["channels"]:
        new_server["channels"].append({"id": channel.idg, "name": channel.name, "member_ids": channel.members})
    for message in server["messages"]:
        new_server["messages"].append(
            {
                "id": message.id,
                "reception_date": message.time,
                "sender_id": message.sender,
                "channel": message.channel,
                "content": message.content,
            }
        )
    with open("server.json", "w", encoding="utf-8") as f:  # écriture du fichier
        json.dump(new_server, f, ensure_ascii=False, indent=2)


def indice(nom: str):  # convertit un nom d'utilisateur en indice utilisateur
    for user in server["users"]:
        if user.name == nom:
            return user.id


def indice_vers_nom(indice: int):
    for user in server["users"]:
        if user.id == indice:
            return user.name


def indice_g(groupe):  # convertit un nom de groupe en indice de groupe
    for group in server["channels"]:
        if group.name == groupe:
            return group.idg


liste_id = [user.id for user in server["users"]]
liste_idg = [group.idg for group in server["channels"]]
liste_idm = [message.id for message in server["messages"]]
liste = [user.name for user in server["users"]]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def generer_id(L: list[int]):  # génère un identifiant user (sécurise liste vide)
    if not L:
        return 1
    return max(L) + 1


def redirection():  # redirige vers le menu principal (affichage centré)
    opts = (
        "Redirections possibles :\n"
        "Affichage utilisateur : Au\n"
        "Affichage messages groupe : Amg\n"
        "Ajouter un utilisateur : Aju\n"
        "Ajouter un groupe : Ajg\n"
        "Ajouter plusieurs utilisateurs : Ajus\n"
        "Retour menu principal : RM\n"
        "Ecriture message : em"
    )
    center_lines(opts, color=CYAN)
    choix = input("Choix : ")
    if choix == "Au":
        affiche_utilisateurs()
    elif choix == "Amg":
        afficher_messages_groupes()
    elif choix == "Aju":
        ajout_utilisateur()
    elif choix == "Ajg":
        ajout_groupe()
    elif choix == "Ajus":
        ajout_plusieurs_utilisateurs()
    elif choix == "em":
        ecriture_message()
    else:
        retour_menu()


def affiche_utilisateurs():  # affichage de tous les utilisateurs
    clear_screen()
    users = [user.name for user in server["users"]]
    if not users:
        center_lines("Aucun utilisateur", color=YELLOW)
        return
    print_list("Liste des utilisateurs", users, color=CYAN)


def afficher_messages_groupes():  # affichage des messages d'un groupe sélectionné
    clear_screen()
    center_lines("Canaux disponibles :", color=GREEN)
    for group in server["channels"]:
        center_lines(f"{group.idg:>3}  -  {group.name}", color=CYAN)
    name_g = input("Choisissez un groupe : ")
    number = indice_g(name_g)
    if number not in liste_idg:
        center_lines("Ce groupe n'existe pas", color=YELLOW)
    else:
        found = False
        for message in server["messages"]:
            if message.channel == number:
                time_sender = f"{message.time} — {indice_vers_nom(message.sender)}"
                center_lines(time_sender, color=BLUE)
                # content peut être liste ou string
                if isinstance(message.content, list):
                    for line in message.content:
                        center_lines(line)
                else:
                    center_lines(message.content)
                center_lines("-" * (_term_width() // 2))
                found = True
        if not found:
            center_lines("Aucun message pour ce groupe", color=YELLOW)


def ajout_utilisateur():
    clear_screen()
    nom = input("Name : ")
    if nom in liste:
        center_lines(f"Utilisateur : {nom} est déjà dans le serveur", color=YELLOW)
        redirection()
        return
    id = generer_id(liste_id)
    user = User(nom, id)
    server["users"].append(user)
    liste.append(nom)
    liste_id.append(id)
    save_server()
    center_lines(f"Utilisateur {nom} ajouté (id={id})", color=GREEN)


def ajout_plusieurs_utilisateurs():
    clear_screen()
    liste_noms = input("Names : ").split(",")
    liste_noms_corr = [user.strip() for user in liste_noms]
    for nom in liste_noms_corr:
        id = generer_id(liste_id)
        user = User(nom, id)
        server["users"].append(user)
        liste_id.append(id)
        liste.append(nom)
    save_server()
    center_lines(f"{len(liste_noms_corr)} utilisateur(s) ajouté(s)", color=GREEN)


def continuer_messagerie(groupe, user):
    choixd = input("Voulez-vous continuer à discuter ? (Oui/Non) :")
    if choixd == "Oui":
        for message in server["messages"]:
            if message.channel == groupe:
                print(message.time, indice_vers_nom(message.sender))
                print("")
                print(message.content)
                print("")
                print("")
        message = input("message :")
        idm = generer_id(liste_idm)
        new_messagerie = Message(groupe, idm, message, str(datetime.now().strftime("%d/%m/%Y %H:%M")), indice(user))
        server["messages"].append(new_messagerie)
        continuer_messagerie(groupe, user)
    else:
        redirection()


def ajout_groupe_et_messagerie_privés():
    clear_screen()
    nom1 = input("Votre prénom : ")
    nom2 = input("Personne avec qui vous voulez parler : ")
    N_ut = []
    if nom2 not in liste:
        N_ut.append(nom2)
    if len(N_ut) == 1:
        center_lines(f"{N_ut} ne fait pas partie des utilisateurs, vous ne pouvez pas discuter avec lui/elle", color=YELLOW)
        redirection()
        return
    nL = [indice(nom2), indice(nom1)]
    cpt = 0
    for group in server["channels"]:
        if group.members == nL or group.members == [indice(nom1), indice(nom2)]:
            cpt += 1
            id_pour_mess = group.idg
    if cpt == 0:  # si le groupe n'existe pas, on le crée
        id_group = generer_id(liste_idg)
        idm = generer_id(liste_idm)
        group_name = input("Nom du groupe : ")
        messages = input("message : ")
        new_group = Channel(group_name, id_group, nL)
        new_messagerie = Message(id_group, idm, [], str(datetime.now().strftime("%d/%m/%Y %H:%M")), indice(nom1))
        server["messages"].append(new_messagerie)
        server["channels"].append(new_group)
        continuer_messagerie(id_group, nom1)
    else:
        idm = generer_id(liste_idm)
        messages = input("message : ")
        new_messagerie = Message(id_pour_mess, idm, messages, str(datetime.now().strftime("%d/%m/%Y %H:%M")), indice(nom1))
        server["messages"].append(new_messagerie)
        continuer_messagerie(id_pour_mess, nom1)
    save_server()


def ajout_groupe():
    clear_screen()
    group_name = input("Name : ")
    id_group = generer_id(liste_idg)
    utilisateurs_group = input("Liste : ").split(",")
    user_corr = [user.strip() for user in utilisateurs_group]
    N_ut = []
    for user in user_corr:
        if user not in liste:
            N_ut.append(user)
    if len(N_ut) == 1:
        center_lines(f"{N_ut} ne fait pas partie des utilisateurs, il faut l'ajouter :", color=YELLOW)
        ajout_utilisateur()
        ajout_groupe()
        return
    elif len(N_ut) > 1:
        center_lines(f"{N_ut} ne font pas partie des utilisateurs, il faut les ajouter :", color=YELLOW)
        ajout_plusieurs_utilisateurs()
        ajout_groupe()
        return
    nL = []
    for x in user_corr:
        nL.append(indice(x))
    new_group = Channel(group_name, id_group, nL)
    server["channels"].append(new_group)
    save_server()
    center_lines(f"Groupe {group_name} ajouté (id={id_group})", color=GREEN)


def ecriture_message():
    clear_screen()
    privé = input("Souhaitez vous parler en privé à un autre utilisateur (Oui/Non) ? :")
    if privé == "Non":
        fuser_name = input("Votre prénom : ")
        center_lines("Groupe(s) disponibles :", color=GREEN)
        for group in server["channels"]:
            if indice(fuser_name) in group.members:
                center_lines(group.name, color=CYAN)
        group_name = input("Quel est le groupe choisi ? :")
        indice_groupe = indice_g(group_name)
        idmes = generer_id(liste_idm)
        message = input("Discussion ouverte :")
        server["messages"].append(
            Message(indice_groupe, idmes, message, str(datetime.now().strftime("%d/%m/%Y %H:%M")), indice(fuser_name))
        )
        continuer_messagerie(indice_groupe, fuser_name)
    else:
        ajout_groupe_et_messagerie_privés()
    save_server()


def retour_menu():
    choix()


def choix():
    print_logo()
    menu = (
        "Sortie du service : S\n"
        "Affichage utilisateurs : u\n"
        "Affichage messages groupe : g\n"
        "Ajout utilisateur : au\n"
        "Ajout Groupe : ag\n"
        "Ajout plusieurs utilisateurs : apu\n"
        "Ecrire un message : em\n"
    )
    center_lines(menu, color=CYAN)
    choice = input("Sélectionnez une option : ")
    if choice == "u":
        affiche_utilisateurs()
        Bol = input("Voulez-vous continuer ? :")
        if Bol == "Oui":
            redirection()
    elif choice == "S":
        center_lines("Sortie du service", color=YELLOW)
    elif choice == "g":
        afficher_messages_groupes()
        Bol = input("Voulez-vous continuer ? :")
        if Bol == "Oui":
            redirection()
    elif choice == "au":
        ajout_utilisateur()
        Bol = input("Voulez-vous continuer ? :")
        if Bol == "Oui":
            redirection()
    elif choice == "apu":
        ajout_plusieurs_utilisateurs()
        Bol = input("Voulez-vous continuer ? :")
        if Bol == "Oui":
            redirection()
    elif choice == "ag":
        ajout_groupe()
        Bol = input("Voulez-vous continuer ? :")
        if Bol == "Oui":
            redirection()
    elif choice == "em":
        ecriture_message()
        Bol = input("Voulez-vous continuer ? :")
        if Bol == "Oui":
            redirection()
    else:
        center_lines(f"Commande inconnue : {choice}", color=YELLOW)
        retour_menu()


choix()