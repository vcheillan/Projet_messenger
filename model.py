class User:
    def __init__(self, name: str, id: str): #crétion de la classe User qui contient tous les élements du dico users
        self.name = name
        self.id = id
    def __repr__(self) -> str:
  #'''Appelée lors de la conversion d'une instance de la classe `User` en `str`. C'est le cas lorsqu'on `print` une instance.'''
        return f'User(name={self.name})'
    

class Channel:
    def __init__(self, name: str, idg: int,members : list): #crétion de la classe Channel qui contient tous les élements du dico channels
        self.name = name
        self.idg = idg
        self.members = members
    def __repr__(self) -> str:
  #'''Appelée lors de la conversion d'une instance de la classe `Channel` en `str`. C'est le cas lorsqu'on `print` une instance.'''
        return f'Channel(name={self.name}, members {self.members})'

class Message:
    def __init__(self, channel: int, id: int,content : list[str], time : str, sender : int): #crétion de la classe Message qui contient tous les élements du dico messages
        self.channel = channel
        self.id = id
        self.content = content
        self.time = time
        self.sender = sender
    
    def __repr__(self) -> str:
  #'''Appelée lors de la conversion d'une instance de la classe `Message` en `str`. C'est le cas lorsqu'on `print` une instance.'''
        return f'Message(Content={self.content})'