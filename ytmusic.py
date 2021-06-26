import datetime
import vlc,time
import threading
from youtube_dl import YoutubeDL 
import sys, os
import pymongo

def logToMDB():
    client = pymongo.MongoClient("mongodb+srv://admin:test@cluster0.mikev.mongodb.net/history?retryWrites=true&w=majority")
    db = client.history.collection1
    logval = {
        "user name": os.getlogin(),
      "song title": "{}".format(sys.argv[1]),
      "time": datetime.datetime.now()
    }

    db.insert_one(logval)

def play():
    ydl_opts = {
        'writesubtitles': False,
        'format': 'mp4',
        'writethumbnail': False
    }

    with YoutubeDL(ydl_opts) as ydl:
        info=ydl.extract_info("ytsearch:%s lyrics" %" ".join(sys.argv[1:]),download=False)['entries'][0]['formats'][0]['url']
        id=ydl.extract_info("ytsearch:%s lyrics" %" ".join(sys.argv[1:]),download=False)['entries'][0]['id']
        duration=ydl.extract_info("https://www.youtube.com/watch?v={sID}".format(sID=id),download=False)['duration']
    player = vlc.MediaPlayer(info)
    player.play()
    time.sleep(duration)

if __name__ == "__main__":

    n = sys.argv[1]
    t1 = threading.Thread(target=logToMDB)
    t2 = threading.Thread(target=play)

    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("done")