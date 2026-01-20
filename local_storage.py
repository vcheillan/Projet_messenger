from datetime import datetime
from model import User
from model import Channel
from model import Message
import json



class LocalStorage: 
    def __init__(self, chemin): #crétion de la classe User qui contient tous les élements du dico LocalStroage
        self.chemin = chemin
    
    def listes_utiles(self):
        server = self.load_server()
        liste_id = [user.id for user in server['users']]

        liste_idg = [group.idg for group in server['channels']]

        liste_idm = [message.id for message in server[' channels']]

        return [liste_id,liste_idg,liste_idm]
    
    def generer_id(self,L):
        return len(L)+1


    def load_server(self):
        server = { 'users':[], 'channels' : [], 'messages' : []}
        with open(self.chemin, "r", encoding = "utf-8") as f: #Lecture du fichier uniquement 
            server1 = json.load(f)
        for user in server1['users']: #conversion du server json en un server local utilisant les classes
            server['users'].append(User(user['name'],user['id'])) 
        for group in server1['channels']:
            server['channels'].append(Channel(group['name'], group['id'], group['member_ids']))
        for message in server1['messages']:
            server['messages'].append(Message(message['channel'],message['id'],message['content'], message['reception_date'], message['sender_id']))
        return server

    def save_server(self,server):
        new_server = { 'users':[], 'channels' : [], 'messages' : []} #conversion inverse afin de changer les classes locales en des dictionnaires
        for user in server['users'] :
            new_server['users'].append({'id' : user.id, 'name' : user.name})
        for channel in server['channels']:
            new_server['channels'].append({'id' : channel.idg, 'name' : channel.name, 'member_ids' : channel.members})
        for message in server['messages']:
            new_server['messages'].append({'id' : message.id, 
                                        'reception_date' : message.time, 
                                        'sender_id' : message.sender, 
                                        'channel' : message.channel,
                                        'content' : message.content})
        with open(self.chemin,"w", encoding = "utf-8") as f: #écriture du fichier --> modification 
            json.dump(new_server, f, ensure_ascii=False, indent=2)


    def get_users(self)-> list[User]:
        return self.load_server()['users']
    
    def create_user(self,name :str)-> int :
        liste_id = self.listes_utilses()[0]
        id = self.generer_id(liste_id)
        dico = self.load_server()
        dico['users'].append(User(name,id))
        return id

    def get_channel(self)-> list[User]:
        return self.load_server()['channels']
    
    def create_channel(self,name):
        liste_id = self.listes_utilses()[1]
        id_channel = self.generer_id(liste_id)
        channel = Channel(name, id_channel, [])
        self.load_server()['channel'].append(channel)
        return id_channel
    
    def add_user_channel(self,user_id ,id_channel):
        server = self.load_server()
        for user in server['users']:
            if user.id == user_id:
                name = user.name
        for channel in server ['channels']:
            if channel.idg == id_channel:
                channel.members.append(User(name, user_id))
            
    
    def get_message(self)-> list[User]:
        return self.load_server()['messages']
    
    def get_channel_message(self, id_channel)-> list[User]:
        server = self.load_server()
        for message in server['messages']:
            if message.channel == id_channel:
                return message.content

    def create_message(self,id_channel, content, sender_id):
        liste_id = self.listes_utilses()[2]
        id_message = self.generer_id(liste_id)
        self.load_server()['messages'].append(Message(id_channel, id_message,content,datetime.now().strftime),sender_id)

