import os
import re
import csv
import logging
import requests
from yt_dlp import YoutubeDL

download_history_csv = "download_history.csv"
mp3_path = "./Music/"
mp4_path = "./Videos/"

if not os.path.exists(mp3_path):
	os.makedirs(mp3_path)
	print("The mp3 download was created successfully!")

if not os.path.exists(mp4_path):
	os.makedirs(mp4_path)
	print("The mp4 download was created successfully!")

if not os.path.isfile(download_history_csv):
	with open(download_history_csv, "w") as csv_file:
		csv_file.close()
		pass

	print("File history csv was created successfully!")


class loggerOutputs:
	logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s", filename="yt-bot.log", encoding="utf-8", level=logging.DEBUG)

	def error(msg):
		print("Error: " + msg)
		logging.error(msg)

	def warning(msg):
		print("Warning: " + msg)
		logging.warning(msg)

	def debug(msg):
		print(msg)

def get_array_from_csv(csv_path):
	array = []

	with open(csv_path) as csv_array:
		for row in csv.reader(csv_array):
			array.append(row)
		csv_array.close()

	return array

def append_to_csv(data, csv_path):
	with open(csv_path, "a") as csv_object:
		writer_object = csv.writer(csv_object)
		writer_object.writerow([data])
		csv_object.close()

def download_mp3(url):
	options = {
		"logger": loggerOutputs,
		"format": "mp3/bestaudio/best",
		"postprocessors": [{
			"key": "FFmpegExtractAudio",
			"preferredcodec": "mp3"
		}],
		"outtmpl": f"{mp3_path}%(artist)s/%(album)s/%(title)s.%(ext)s",
		"concurrent_fragment_downloads": 4
	}

	YoutubeDL(options).download(url)
	append_to_csv(url, download_history_csv)

def download_mp4(url):
	options = {
		"format": "bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4+best[height<=480]",
		"logger": loggerOutputs,
		"outtmpl": f"{mp4_path}%(title)s.%(ext)s",
		"concurrent_fragment_downloads": 4
	}

	YoutubeDL(options).download(url)
	append_to_csv(url, download_history_csv)

def download_mp4_playlist(url: str) -> map:
	# since it uses a set it's not ordered
	# since youtube doesn't provide more than 100 links at the time for the moment
	# it returns up to 100 elements
	page_text = requests.get(url).text

	parser = re.compile(r"watch\?v=\S+?list=")
	playlist = set(re.findall(parser, page_text))
	playlist = map((lambda x: "https://www.youtube.com/" + x.replace("\\u0026list=", "")), playlist)

	for u in playlist:
		download_mp4(u)

def download_from_csv(csv_path):
  with open(csv_path, "r") as f:
    reader = csv.reader(f, delimiter="\n")
    for url in reader:
      for u in url:
        download_mp4(u)

def main():
	try:
		while True:
			url = input("Please enter a video link or type 'exit' to quit: ")

			if [url] in get_array_from_csv(download_history_csv):
				print("This video has already been downloaded!")
			else:
				if "music.youtube.com" in url:
					download_mp3(url)
				elif "playlist?" in url:
					download_mp4_playlist(url)
				elif(url == "exit"):
					break
				elif(url == "csv"):
				  download_from_csv("todo.csv")
				else:
					download_mp4(url)

	finally:
		print("Thanks for using yt-bot!")

main()
