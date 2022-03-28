from pytube import YouTube
import urllib.request
import re
import subprocess
import os
import requests
import bs4
from pathlib import Path

def search_youtube(track):
    print("https://www.youtube.com/results?search_query={}".format(track))
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query={}".format(track))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return video_ids


def convert_to_mp3(title):
    try:
        return subprocess.run([
            'ffmpeg',
            '-i', os.path.join(parent_dir, title + ".mp4"),
            os.path.join(parent_dir, title + ".mp3")
        ])
    except subprocess.CalledProcessError as e:
        return title + " cannot be converted."


def check_mp3_exists(file_name):
    file_name = file_name + ".mp4"
    path = Path("/Users/######/######/{}".format(file_name))
    if path.is_file():
        return True
    else:
        return False


def remove_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])


genre_links = []
parent_dir = "/Users/######/######/"

top_url = "https://soundcloud.com/charts/top"
request = requests.get(top_url)
soup = bs4.BeautifulSoup(request.text, "lxml")

# retrieve all genres from the soundcloud top chart
genres = soup.select("a[href*=genre]")[2:]

for index, genre in enumerate(genres):
    genre_links.append(genre.get("href"))

# only get genre link for hip-hop & rap
genre_link = [s for s in genre_links if "hiphoprap" in s][0]

url = "http://soundcloud.com" + genre_link
request = requests.get(url)
soup = bs4.BeautifulSoup(request.text, "lxml")

# all the tracks are associated to h2 tag in the html source
tracks = soup.select("h2")[3:]
# holds soundcloud track links
track_links = []
# holds soundcloud track names
track_names = []
formatted_track_names = []

for index, track in enumerate(tracks):
    track_links.append(track.a.get("href"))
    track_names.append(track.text)

print(track_names)
if len(track_names) > 0:
    formatted_track_names = [track.replace('\r', '').replace('\n', ' ') for track in track_names]
else:
    print("SoundCloud Top Charts does not have the track names.")

if formatted_track_names and len(formatted_track_names) == 50:
    for track_name in formatted_track_names[0:20]:
        track_name = remove_ascii(track_name)
        print("Processing track {}.".format(track_name))
        formatted_track = "+".join(track_name.split(" "))

        # search YouTube using the track name
        yt_video_ids = search_youtube(formatted_track)

        # check if YouTube has the track link for given track name
        if len(yt_video_ids) > 0:
            url = "https://www.youtube.com/watch?v={}".format(yt_video_ids[0])
            print(url)
            video = YouTube(url)
            streams = video.streams.filter(only_audio=True, file_extension="mp4").order_by("abr").all()
            title = streams[-1].title
            streams[-1].download(parent_dir)
            if title and check_mp3_exists(title):
                convert_to_mp3(title)
            else:
                print("Mp4 file not exists for {}.".format(title))
        else:
            print("{} is not uploaded in YouTube yet.".format(formatted_track))
else:
    print("Formatted tracks is not of size 50.")