import os
import csv
from yt_dlp import YoutubeDL

download_history_csv = "download_history.csv"

if not os.path.isfile(download_history_csv):
	with open(download_history_csv, "w") as csv_file:
		csv_file.close()
		pass

	print("File history csv was created successfully!")

class loggerOutputs:
	def error(msg):
		print("Error: " + msg)

	def warning(msg):
		print("Warning: " + msg)

	def debug(msg):
		print(msg)

def get_array_from_csv(csv_path):
	array = []

	with open(csv_path) as csv_array:
		reader = csv.reader(csv_array)

		for row in reader:
			array.append(row)
		csv_array.close()

	return array

def append_to_csv(data, csv_path):
	row = [data]
	with open(csv_path, "a") as csv_object:
		writer_object = csv.writer(csv_object)
		writer_object.writerow(row)
		csv_object.close()


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
		download_history_array = get_array_from_csv(download_history_csv)
		print(download_history_array)

		while True:
			url = input("Please enter a video link or type 'exit' to quit: ")

			if (url != "exit"):
				download_mp4(url)
				append_to_csv(url, download_history_csv)

			elif(url == "exit"):
				break

	finally:
		print("Thanks for using yt-bot!")

main()
