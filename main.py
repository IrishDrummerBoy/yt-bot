from yt_dlp import YoutubeDL

def format_selector(ctx):
	""" Select the best video and the best audio that won't result in an mkv.
	NOTE: This is just an example and does not handle all cases """

	# formats are already sorted worst to best
	formats = ctx.get('formats')[::-1]

	# acodec='none' means there is no audio
	best_video = next
	(
		f for f in formats
			if f['vcodec'] != 'none' and f['acodec'] == 'none'
	)

	# find compatible audio extension
	audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
	# vcodec='none' means there is no video
	best_audio = next(f for f in formats if (
		f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))

	# These are the minimum required fields for a merged format
	yield {
		'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
		'ext': best_video['ext'],
		'requested_formats': [best_video, best_audio],
		# Must be + separated list of protocols
		'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
	}

def download_all_songs(urls):
	ydl_opts = {
		'format': 'mp3/bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3'
		}]
	}

	YoutubeDL(ydl_opts).download(urls)

def main():
	# movie_playlist_urls = [""]
	url = []

	YoutubeDL().download(url)

	while True:
		url = input("Please enter a video link or type 'exit' to quit: ")

		if (url != "exit"):
			YoutubeDL().download(url)
		elif(url == "exit"):
			break

	print("Thanks for using yt-bot!")
main()
