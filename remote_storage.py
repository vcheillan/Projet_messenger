import requests
from model import User
from model import Channel
from model import Message
class RemoteStorage: 
    def get_users(self)-> list[User]:
        liste = []
        response = requests.get("https://groupe5-python-mines.fr/users")
        for dico in response.json():
            liste.append(User(dico['name'],dico['id']))
        return liste
    
    def create_user(self,name :str)-> int :
        user = {'name' : name}
        response = requests.post("https://groupe5-python-mines.fr/users/create",json = user)
        return response.json()['id']

    def get_channel(self)-> list[User]:
        liste = []
        response = requests.get("https://groupe5-python-mines.fr/channels")
        #print(response.json())
        for dico in response.json():
            members = requests.get(f"https://groupe5-python-mines.fr/channels/{dico['id']}/members").json()
            #print(members)
            liste.append(Channel(dico['name'],dico['id'],members))
            #print(Channel(dico['name'],dico['id'],members))  
        return liste
    def create_channel(self,name, id_channel):
        channel = {'name' : name, 'id' : id_channel }
        requests.post("https://groupe5-python-mines.fr/channels/create",json = channel)
        print(requests.post("https://groupe5-python-mines.fr/channels/create",json = channel))
    
    def add_user_channel(self,user_id ,id_channel):
        user = {'user_id' : user_id}
        post_user = requests.post(f"https://groupe5-python-mines.fr/channels/{id_channel}/join",json = user )
        print(post_user.text)
    
    def get_message(self)-> list[User]:
        liste = []
        response = requests.get("https://groupe5-python-mines.fr/messages")
        for dico in response.json():
            liste.append(Message(dico['channel_id'],dico['id'], dico['content'], dico['reception_date'], dico['sender_id']))
        return liste
    
    def get_channel_message(self, id_channel)-> list[User]:
        liste = []
        response = requests.get(f"https://groupe5-python-mines.fr/channels/{id_channel}/messages")
        for dico in response.json():
            liste.append(Message(dico['channel_id'],dico['id'], dico['content'], dico['reception_date'], dico['sender_id']))
        return liste

    def create_message(self,id_channel, content, sender_id):
        message = {'sender_id':sender_id, 'content' : content }
        requests.post(f"https://groupe5-python-mines.fr/channels/{id_channel}/messages/post",json = message)
