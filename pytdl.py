import sys

from pytube import YouTube, Playlist
from progressbar import ProgressBar

command, *args = sys.argv

if '-h' in args or '--help' in args:
    print("\033[H\033[J") # clear term screen
    print('''    \033[1mWelcome to your lightweight YouTube downloader!\033[0m
    A command-line interface to download YouTube videos (in mp4 video/audio formats).

    \033[1mUSAGE\033[0m
    pytdl [URL] [PATH] [OPTIONS]

    \033[1mSUPPORTED OPTIONS\033[0m
    [-a, --audio]       Download the stream as a mp4 audio-only file
    [-h, --help]        Show this screen

    ''')
    sys.exit()

if len(args) < 1:
    print('No URL was passed!')
    sys.exit()

url, output_path, *options = args
bar = ProgressBar(max_value=100)

user_options = {
    'audio': '-a' in options or '--audio' in options
} if options else {}

download_type = 'audio' if user_options.get('audio') else 'video'
audio_quality_filter = {
    'mime_type': 'audio/mp4',
}
video_quality_filter = {
    'mime_type': 'video/mp4',
}

def on_progress(stream, chunk, bytes_remaining):
    progress = round((1 - bytes_remaining / stream.filesize) * 100, 3)
    bar.update(progress)

def get_best_quality(video):
    if user_options.get('audio'):
        return video.streams.filter(**audio_quality_filter).first()

    return video.streams.filter(progressive=True, **video_quality_filter).order_by('resolution').desc().first()

def download_video(video_url):
    try:
        video = YouTube(video_url, on_progress_callback=on_progress)
    except:
        print("Couldn't find URL {0}!".format(video_url))
        sys.exit()
    print('Downloading {0} from "{1}"'.format(download_type, video.title))
    video_stream = get_best_quality(video)
    try:
        video_stream.download('{0}/'.format(output_path))
    except Exception as error:
        print(error)
    sys.exit()

if 'playlist' in url:
    playlist = Playlist(url)
    
    for video_url in playlist:
        download_video(video_url)

    sys.exit()

download_video(url)