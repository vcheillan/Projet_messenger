from datetime import datetime

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

print('=== Messenger ===')
print('x. Leave')
choice = input('Select an option: ')
if choice == 'x':
    print('Bye!')
elif choice == 'u':
    for dico in server['users']:
        print(dico['name'])
elif choice == 'g':
    for dico in server['channels']:
        print(dico['name'])
else:
    print('Unknown option:', choice)
