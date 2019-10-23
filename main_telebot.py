import time
import telebot
import logging
import requests
import datetime
from telebot import types
from easyjwt import EasyJWT
from logging import Handler, Formatter
import pyotp

totp = pyotp.TOTP("JBSWY3DPEHPK3PXP",interval=120)
token = totp.now()
print("Current OTP:", token)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) #

TOKEN = '970406731:AAGRJVcUeDSnWZP39x70jRdcfvlmECVLHNQ'

keyIn = []

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
    'start'       : 'Get used to the bot',
    'help'        : 'Gives you information about the available commands',
    'sendLongText': 'A test using the \'send_chat_action\' command',
    'getImage'    : 'Today image!',
    'getVideo'    : 'Today video!',
    'getProverb'  : 'Message of the day'
}


def filesave():
    print(knownUsers)
    with open("chat_id.txt", "a") as knownUser_file:
        for line in knownUsers:
            knownUser_file.write('%d\n' % int(line))

def fileread():
    with open("chat_id.txt", 'rb') as user_data:
        global knownUsers
        for user in user_data.read().split():
            knownUsers.append(int(user))
        print(knownUsers)
        """for user in knownUsers:
            sendAuto_message(user, "Every successful hardware has a software behind.")"""

# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener

def auth(m):
    cid = m.chat.id
    global keyIn
    keyIn = m.text
    if totp.verify(keyIn): # => True.verify():
        knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
        userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
        bot.send_message(cid, "Hello, stranger, let me scan you...")
        bot.send_message(cid, "Scanning complete, I know you now")
        command_help(m)
        print(knownUsers)
        filesave()
    else:
        return bot.send_message(cid ,'Code has expired or is incorrect!')


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid in knownUsers:  # if user hasn't used the "/start" command yet:
        bot.send_message(cid, 'You are logged in!')
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "I already know you, no need for me to scan you again!")
    else:
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        msg = bot.send_message(cid ,'Hello, Please enter the code you received by SMS or E-mail.')
        bot.register_next_step_handler(msg, auth)

# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    if cid in knownUsers:
        help_text = "The following commands are available: \n"
        for key in commands:  # generate help text out of the commands dictionary defined at the top
            help_text += "/" + key + ": "
            help_text += commands[key] + "\n"
        bot.send_message(cid, help_text)  # send the generated help page
    else:
        bot.send_message(m.chat.id, "You are not authorized to login. Please create a new code on the device. If you have the code, you can log in by typing /start .")


# chat_action example (not a good one...)
@bot.message_handler(commands=['sendLongText'])
def command_long_text(m):
    cid = m.chat.id
    if cid in knownUsers:
        bot.send_message(cid, "If you think so...")
        bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
        time.sleep(3)
        bot.send_message(cid, ".")
    else:
        bot.send_message(m.chat.id, "You are not authorized to login. Please create a new code on the device. If you have the code, you can log in by typing /start .")


# user can chose an image (multi-stage command example)
@bot.message_handler(commands=['getImage'])
def command_image(m):
    cid = m.chat.id
    if cid in knownUsers:
        bot.send_chat_action(cid, 'typing')
        bot.send_photo(cid, open('media/robot.jpg', 'rb'))
        bot.send_photo(cid, open('media/xp.jpg', 'rb'))
        userStep[cid] = 1  # set the user to the next step (expecting a reply in the listener now)
    else:
        bot.send_message(m.chat.id, "You are not authorized to login. Please create a new code on the device. If you have the code, you can log in by typing /start .")


@bot.message_handler(commands=['getVideo'])
def command_video(m):
    cid = m.chat.id
    if cid in knownUsers:
        bot.send_chat_action(cid, 'typing')
        bot.send_video(cid, open('media/animation.mp4', 'rb'))
        userStep[cid] = 0
    else:
        bot.send_message(m.chat.id, "You are not authorized to login. Please create a new code on the device. If you have the code, you can log in by typing /start .")


# filter on a specific message
@bot.message_handler(func=lambda message: message.text == "hi")
def command_text_hi(m):
    if cid in knownUsers:
        bot.send_message(m.chat.id, "Hi bro what's up?")
    else:
        bot.send_message(m.chat.id, "You are not authorized to login. Please create a new code on the device. If you have the code, you can log in by typing /start .")

@bot.message_handler(commands=['getProverb'])
def command_text_test(m):
    cid = m.chat.id
    if cid in knownUsers:
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "Software comes from heaven when you have good hardware :)")
        bot.send_chat_action(cid, 'typing')
        time.sleep(2)
        bot.send_message(cid, "Ken Olsen")
    else:
        bot.send_message(m.chat.id, "You are not authorized to login. Please create a new code on the device. If you have the code, you can log in by typing /start .")

#############################################################################################################
# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    cid = m.chat.id
    if cid in knownUsers:
        bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")
    else:
        bot.send_message(m.chat.id, "You are not authorized to login. Please create a new code on the device. If you have the code, you can log in by typing /start .")


#Execute functions
fileread()
print(knownUsers)
bot.polling()
