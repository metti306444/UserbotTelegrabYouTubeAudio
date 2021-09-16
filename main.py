from pyrogram import Client, filters
import os

import youtube_dl
import shutil

def convert(URL = ""):
	if "watch?v=" in URL: 
		return URL.split('watch?v=')[1][:11]
	if "youtu.be/" in URL: 
		return URL.split('youtu.be/')[1][:11]

def download_audio(URL):
	ydl_opts = {
			'format': 'bestaudio/best',
			'download_archive': 'temp/downloaded_songs.txt',
			'outtmpl': "temp/%(id)s.%(ext)s",
			'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': "mp3",
			'preferredquality': '192',
			}],
			
		}
	
	
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		info2 = ydl.extract_info(URL, download=True)
	
	

	return info2
	
	
def get_info_list(URL):
	ydl_opts = {
		'ignoreerrors': True,
		'quiet': True
		}

	res = []
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		info2 = ydl.extract_info(URL, download=False)

		for video in info2['entries']:
			res.append(video["id"])
	return res

			


def createTemp():
	try:
		os.mkdir("temp")
	except Exception as e:
		pass
	



app = Client("my_account")
app2 = Client("my_account")	
	
@app.on_message(filters.me & filters.command("get", prefixes="."))
def audio(client, message):
	createTemp()
	try:
		

		link = "https://www.youtube.com/watch?v=" + convert(message.text[10:])
		
		ss = message.reply_text("Скачиваю...")
		info = download_audio(link)
		
		fileName = "temp/"+info["id"]+".mp3"
		
		ss.edit(text = "Отправляю...")
		try:
			client.send_audio(message["chat"]["id"], fileName, title=""+info['alt_title'], performer=info['artist'])
		except Exception as e:
			client.send_audio(message["chat"]["id"], fileName, title=""+info['title'], performer=info['uploader'])

		ss.delete()
	except Exception as e:
		print(e)

	shutil.rmtree('temp')



@app.on_message(filters.me & filters.command("getPlayList", prefixes="."))
def PlayList(client, message):
	ss = message.reply_text("Получаю инфу о плейлисте...")
	createTemp()
	try:
		
		playlist = message.text[13:]
		links = get_info_list(playlist)

		i = 1
		ss.delete()
		for link in links:
			title = "**Обработка:** " + str(i) + " из " + str(len(links)) + "\n"
			ss = message.reply_text(title + "**Статус:** Скачиваю...")

			link = "https://www.youtube.com/watch?v=" + link
			try:
				info = download_audio(link)
			except Exception as e:
				ss.edit(text = title + "**Статус:** Обработать не удалось")
				continue
			

			fileName = "temp/"+info["id"]+".mp3"

			ss.edit(text = title + "**Статус:** Отправляю трек...")
			try:
				client.send_audio(message["chat"]["id"], fileName, title=""+info['alt_title'], performer=info['artist'])
			except Exception as e:
				client.send_audio(message["chat"]["id"], fileName, title=""+info['title'], performer=info['uploader'])

			ss.delete()
			i += 1
			
	except Exception as e:
		print(e)

	shutil.rmtree('temp')

text = """**Юзербот[ ](https://telegra.ph/file/e2c7f916e5e7176e6dc91.mp4)для скачивание треков с ютуба запущен**

Программа поддерживает 2 команды:
.get - скачать трек
.getPlayList - скачать плейлист
Ниже приведен пример использования команд

Детальная информация про данное ПО находится [по этой ссылке](https://telegra.ph/YUzerbot-dlya-skachivaniya-trekov-s-YouTube-09-16)"""
with app2 as app2:
	app2.send_message("me", text)

app.run()