from datetime import datetime
import os
from model import User, Message, Channel   
from remote_storage import RemoteStorage
from local_storage import LocalStorage
import pytest

Remote = RemoteStorage("https://groupe5-python-mines.fr/")

def test_get_users():
    users = Remote.get_users()
    assert type(users) == list
    for user in users:
        assert type(user) == User

def test_create_user():
    user_id = Remote.create_user("TestUser")
    assert type(user_id) == int
    users = Remote.get_users()
    user_ids = [user.id for user in users]
    assert user_id in user_ids

def test_get_channel():
    channels = Remote.get_channel()
    assert type(channels) == list
    for channel in channels:
        assert type(channel) == Channel

def test_create_channel():
    channel_id = Remote.create_channel("TestChannel")
    assert type(channel_id) == int
    channels = Remote.get_channel()
    channel_ids = [channel.idg for channel in channels]
    assert channel_id in channel_ids


def test_add_user_channel():
    user_id = Remote.create_user("ChannelUser")
    channel_id = Remote.create_channel("ChannelForUser")
    Remote.add_user_channel(user_id, channel_id)
    channels = Remote.get_channel()
    for channel in channels:
        #vérifie que l'user a été rajouté dans le bon groupe
        if channel.idg == channel_id:
            assert user_id in channel.members
    
def test_get_message():
    messages = Remote.get_message()
    assert type(messages) == list
    for message in messages:
        assert type(message) == Message

def test_get_channel_message():
    channels = Remote.get_channel()
    id_channel = channels[0].idg
    messages = Remote.get_channel_message(id_channel)
    assert type(messages) == list
    for message in messages:
        assert type(message) == Message
    
def test_create_message():
    user_id = Remote.create_user("MessageUser")
    channel_id = Remote.create_channel("MessageChannel")
    Remote.add_user_channel(user_id, channel_id)
    Remote.create_message(channel_id, ["Test."], user_id)
    messages = Remote.get_channel_message(channel_id)
    contents = [message.content for message in messages]
    assert ["Test."] in contents
    for message in messages:
        if message.content == ["Test."]:
            assert message.sender == user_id
            assert message.channel == channel_id



