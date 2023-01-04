from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

class loggerOutputs:
	def error(msg):
		print("Captured Error: " + msg)

	def warning(msg):
		print("Captured Warning: " + msg)

	def debug(msg):
		print("Captured Log: " + msg)

def download_mp3(url):
	options = {
		"logger": loggerOutputs,
		"format": "mp3/bestaudio/best",
		"postprocessors": [{
			"key": "FFmpegExtractAudio",
			"preferredcodec": "mp3"
		}]
	}

	YoutubeDL(options).download(url)

def download_mp4(url):
	options = {
		"format": "bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4+best[height<=480]",
		"logger": loggerOutputs
	}

	YoutubeDL(options).download(url)

def main():
	try:
		while True:
			url = input("Please enter a video link or type 'exit' to quit: ")

			if (url != "exit"):
				download_mp4(url)
			elif(url == "exit"):
				break

	except DownloadError:
		print(DownloadError)

	finally:
		print("Thanks for using yt-bot!")

main()
