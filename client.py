import socket
import json
import time
import os
from datetime import datetime

a = 0 


def send_command(command, data=None):
    req = {'command': command, 'data': data}
    req = json.dumps(req).encode()
    sock = socket.socket()
    sock.connect(('localhost', 1717))
    sock.sendall(req)

    res = b''
    while True:
        buf = sock.recv(1024)
        if buf == b'':
            break
        else:
            res += buf
    return json.loads(res.decode())


def main():
    while True:
        os.system('clear') 
        x = datetime.now()
        day = x.strftime('%A')
        date = x.strftime('%d-%m-%Y')
        print("                    Hi There !                     ")
        print(f"    What Activities are You Gonna Do on {day}?    ")
        print("---------------------------------------------------")
        print("           Today's date is : ", date, "\n")
        print(viewList())
        print("              What do you want to do?              ")
        print("---------------------Commands----------------------")
        print("   view | add {date} {desc} | delete {id} | exit   ")
        print("""
    > view : Updates the list\n
    > add : Add an Activity with date 
    (DD-MM-YYYY) and description  \n
    > delete: Delete an Activity according to id \n
    > exit: Exit the program""")
        print("---------------------------------------------------")
        comin = input("Type the Command: ")
        comin = comin.split(' ', 2)  
        if not comin[0].isalnum() or not comin: 
            continue
        if comin[0] == 'view': 
            continue
        elif comin[0] == 'add':
            add_menu(comin[1], comin[2])
        elif comin[0] == 'delete':
            if len(comin) < 2:
                continue
            delete_menu(comin[1])
        elif comin[0] == 'exit':
            print('Thank you, have a nice day \:3')
            break
        else:
            print('Invalid Command!')
        time.sleep(1)


def viewList():
    data = send_command('view')
    global a
    message = ''
    print("Activities List :\n")
    a = len(data['data'])
    if (len(data['data'])) > 0:  
        message += "+--------+--------+--------+--------+\n"
    for x in range(len(data['data'])):
        message += f"\t Date \t\t : {data['data'][x]['date']}\n" \
                   f"\t Description : {data['data'][x]['desc']}\n" \
                   f"\t Activity Id : {data['data'][x]['id']}\n" \
                   f"+--------+--------+--------+--------+\n"

        if data['data'][x]['id'] > a:
            a = data['data'][x]['id']
    return message


def add_menu(date_str, desc):
    global a
    id = a + 1
    while True:  
        try:
            datetime.strptime(date_str, '%d-%m-%Y').date() 
        except Exception as e:
            print("Warning: ", e)
        else:
            break
    # JSON format
    dictionary = {"date": date_str, "desc": desc, "id": id}
    print(f'Id of the Activity is automatically set to {id}')
    respond = send_command('add', dictionary)

    if respond['ok']:
        print(f'Successfully added an Activity with id: {id}')
    else:
        print('Error')


def delete_menu(id):
    global a
    # Handle id
    if not id.isdigit():
        print('id must be an unsigned integer')
        return
    id = abs(int(id))

    # JSON format
    dictionary = {"id": id}
    respond = send_command('delete', dictionary)

    if respond['ok']:
        print(f'Sucessfully removed an Activity with id: {id}')
    else:
        print('Error')


def get_non_negative_int(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if value < 0:
            print("Sorry, your response must not be negative.")
            continue
        else:
            break
    return value


main()
