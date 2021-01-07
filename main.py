#!/usr/bin/env python3

#doing all needed imports
from os import system
from firebase import firebase
import threading
from pygame import mixer
import subprocess as s
from sys import argv
from datetime import datetime

#we need it to that thing down here
sound = True

#here's that thing. If you don't want notification sound - turn off it!
if len(argv) > 1:
    if argv[1] == "--notification-sound-off":
        sound = False

#initialising our mixer for notification sound
mixer.init()

#we need it to generate number for user
username = ' ' + input("Type in your username: ") + ": "

while " " in username.strip():
    username = ' ' + input("Type in your username (you cannot separate words with spaces): ") + ": "

#it's "cls" for windows, here we'll clear console to everything looks ok
system("clear")

#thanks to Python code won't work if this line doesn't exist
result = "\nSEND MESSAGE\n"

#we're creating db for our messages
fb = firebase.FirebaseApplication("https://dbcfv-60641-default-rtdb.europe-west1.firebasedatabase.app/", None)

#it is our old data so we can compare it with new and messages will be updated
old_data = {} 

#it's a function where we take user's input
def get_input_from_the_user():
    while True:
        #now we're asking for message and add user number
        message = input("Type your message:   ")
        
        if "(yes)" in message:
            message = message.replace("(yes)", "👍")
        if "(y)" in message:
            message = message.replace("(y)", "👍")
        if "(no)" in message:
            message = message.replace("(no)", "👎")
        if "(cryingwithlaughter)" in message:
            message = message.replace("(cryingwithlaughter)", "😂")

        if message == "/clear":
            fb.delete('Message', '')

        if message.startswith("/edit"):
            message_id = ""
            message = message.split()
            if len(message) > 3:
                time_and_username = message[1] + " " + message[2]
                if username.startswith(message[2]):
                    edited_message = ""
                    for word in message:
                        if message.index(word) > 2:
                            edited_message += word + " "
                    for msg in messages:
                        if messages[msg]["Message"].startswith(time_and_username):
                            message_id = msg
                    fb.put(f'Message/{message_id}/', 'Message', str(datetime.now().time())[:8] + username + "EDITED " + edited_message)

        else:
            Smessage = str(datetime.now().time())[:8] + username + message

            #it is our data with messages
            data = {
                'Message':Smessage
            }

            #as you can see we post out message to db
            fb.post('Message', data)

#thanks to this line we can do 2 things (get input and print messages) at once
thread = threading.Thread(target=get_input_from_the_user)
thread.start()

#here's our notification sound (you need to download needed file)
mixer.music.load("noti2.wav")

#here's our loop so we'll be able to send messages over and over again
while True: 
    #we're taking messages from db
    messages = fb.get(f'/Message/', '')

    #if messages came:
    if messages:
        if old_data != messages: #if sth new in messages:
            try:
                message = messages[list(messages.keys())[-1]]["Message"]
                print(message)
                author = message.split()[1].strip()
                if " " + author + " " != username:
                    #create notification banner
                    s.call(['notify-send','Perfect Messenger', message])
                    if sound: mixer.music.play(0) #and here's sound if it turned on
                #it's "cls" for windows, here we'll clear console to everything looks ok
                system('clear')
                for message in messages:
                    print(messages[message]["Message"])

                old_data = messages
                print(result)
            except Exception as e:
                print(e)
