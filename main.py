import os
import configparser
import asyncio
import questionary

from telethon import TelegramClient
from telethon import errors

if os.path.exists('config.ini'):
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_id = config['TelegramApi']['api_id']
    api_hash = config['TelegramApi']['api_hash']
else:
    api_id = int(questionary.password('Api ID:').ask())
    api_hash = questionary.password('Api hash:').ask()

    config = configparser.ConfigParser()
    config['TelegramApi'] = {'api_id': api_id,
                             'api_hash': api_hash,
                             }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

client = TelegramClient('session_new', api_id, api_hash)
client.start()

print('Bot started')


async def main():
    # absolute_path_file = os.path.abspath("images/pic.jpg")
    channel = '<Channel Name>'
    image_link = None
    message = ''
    with open('message.txt', encoding='utf-8') as f:
        for line in f:
            message += line

    await client.get_dialogs()

    me = await client.get_me()
    participants = await client.get_participants(channel)
    for x in participants:
        if x == me or 'bot' in x.username:
            continue
        async with client.action(x.id, 'typing'):
            try:
                await asyncio.sleep(2)
                await client.send_message(x.id, message[:1024], file=image_link)
                print('Message was sent successfully!!!')
            except errors.FloodWaitError as e:
                print('Flood for', e.seconds)
            except errors.MediaCaptionTooLongError as e:
                print('Your text is too long', e)

with client:
    client.loop.run_until_complete(main())
