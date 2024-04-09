import shutil
import random
import os
import webbrowser
from config import *


with open("message_sample.html", "r") as messageFile:
        message_sample = messageFile.read()

with open("messages.txt", "r", encoding="utf-8") as file:
    messages = file.read().splitlines()

with open("rare_messages.txt", "r", encoding="utf-8") as file:
    rare_messages = file.read().splitlines()

shutil.copy2("Telegram_Web.html", RES_FILENAME, follow_symlinks=True)

with open(RES_FILENAME, 'r') as res_file:
    main_html = res_file.read()


message_list_str = ""

rare_messages_pos = random.sample(range(MESSAGE_COUNT), len(rare_messages))

current_reactions_count = REACTINS_MAX

for i in range(MESSAGE_COUNT):
    if random.randint(1, 20) == 1:
        MESSAGE_TIME = time.localtime(time.mktime(MESSAGE_TIME) + 60)

    random_avatar_filename = os.path.join("avatars", random.choice(os.listdir("avatars")))
    nickname = os.path.splitext(os.path.basename(random_avatar_filename))[0] # Nickname is defined with avatar filename

    avatar_url = random_avatar_filename.replace(' ', '%20').replace('#', '%23')

    if i in rare_messages_pos:
        message_text = rare_messages.pop()
    else:
        message_text = random.choice(messages)

    current_reactions_count = REACTIONS_MIN + int((REACTINS_MAX - REACTIONS_MIN) / (i+1)) + (1 if random.randint(1, 20) == 1 and i!=0  else 0)  # Parabolic distribution of number + random fluxtuations

    message = message_sample.format(avatar=avatar_url, text=message_text, time=time.strftime("%H:%M", MESSAGE_TIME), nickname=nickname, reactions=current_reactions_count)
    message_list_str += message + '\n'

with open(RES_FILENAME, 'w', encoding="utf-8") as file:
    file.write(main_html.replace("[message_list_str]", message_list_str))

webbrowser.open("result.html")