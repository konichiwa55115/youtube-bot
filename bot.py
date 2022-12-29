import os
import pytube
import config
from moviepy.editor import *
from telethon import TelegramClient, events, Button
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',level=logging.WARNING)

bot = TelegramClient('bot', 17983098, "ee28199396e0925f1f44d945ac174f64").start(bot_token="5793890668:AAG0Tl-27fOWdy5cfCDd7Zfwo5qaOAM_n6o")

def download(url):
    # download a song from a given url
    yt = pytube.YouTube(url).streams.filter().all()[0]
    print('Downloading {}'.format(yt.title))
    yt.download(filename='song')
    video = VideoFileClip('song.mp4')
    video.audio.write_audiofile(yt.title+'.mp3')
    print('done!')
    return yt.title

async def download_song(conv):
    try:
        await conv.send_message('Please send me a youtube link to the song')
        link = await conv.get_response()
        await conv.send_message('Downloading... this may take some time')
        link = link.text
        title = download(str(link))
        await conv.send_file(title+'.mp3')
        os.remove(title+'.mp3')
        os.remove('song.mp4')
    except Exception as e:
        print(e)
        await conv.send_message("error... please make sure you insert a correct url")

async def send_buttons(conv):
    await conv.send_message('Please choose one of the buttons', buttons=[Button.text('Download a song',resize=True), Button.text('Download a playlist')])
    ans = await conv.get_response()
    return ans.text

async def download_playlist(conv):
    try:
        await conv.send_message('Please send me a youtube link to the playlist')
        link = await conv.get_response()
        await conv.send_message('Downloading... this may take some time')
        link = link.text
        pl = pytube.Playlist(link)
        pl.download_all('playlists/')
        for song in os.listdir('playlists/'):
            old_file = os.path.join('playlists', song)
            new_file = os.path.join('playlists', song[1:])
            os.rename(old_file, new_file)
        for song in os.listdir('playlists/'):
            print(song)
            video = VideoFileClip('playlists/'+song)
            video.audio.write_audiofile('playlists/'+song.replace(".mp4","")+'.mp3')
            await conv.send_file('playlists/'+song.replace(".mp4","")+'.mp3')
            os.remove('playlists/'+song.replace(".mp4","")+'.mp3')
            os.remove('playlists/'+song)
    except Exception as e:
        print(e)
        await conv.send_message("error... please make sure you insert a correct url")

@bot.on(events.NewMessage(pattern='/start'))
async def handler(event):
    async with bot.conversation(event.chat, timeout=None) as conv:
        await conv.send_message('Hi I will download any youtube audio file you wish in mp3 format')
        while True:
            user_choice = await send_buttons(conv)
            if user_choice == 'Download a song':
               await download_song(conv)
            elif user_choice == "Download a playlist":
               await download_playlist(conv)

bot.run_until_disconnected()
