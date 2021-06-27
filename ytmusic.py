import datetime
import vlc,time
import threading
from youtube_dl import YoutubeDL 
import sys, os
import pymongo
from dotenv import load_dotenv
load_dotenv('./.env')
#Logging into MongoDb
def logToMDB():
    if(sys.argv[1] not in ["-p", "-s","-d"]):
        return
    isPlaylist = True if (sys.argv[1] == '-p') else False
    client = pymongo.MongoClient(os.getenv('mongouri'))
    db = client.history.collection1
    if(isPlaylist):
        logval = {
            "user name": os.getlogin(),
            "playlist url": "{}".format(sys.argv[2]),
            "time": datetime.datetime.now()
        }
    else :
        logval = {
            "user name": os.getlogin(),
            "song title": "{}".format( " ".join(sys.argv[2:])),
            "time": datetime.datetime.now()
        }

    db.insert_one(logval)

#Function to play song
def play():
    ydl_opts = {
        'outtmpl': './downloads/%(title)s.%(ext)s',
        'writesubtitles': False,
        'format': 'm4a',
        'writethumbnail': False
    }

    with YoutubeDL(ydl_opts) as ydl:
        if(sys.argv[1]=="-p"):
            duration=0
            info=[]
            for entries in ydl.extract_info("%s"  % " ".join(sys.argv[2:]),download=False)['entries']:
                info=(entries['formats'][0]['url'])
                id=entries['id']
                duration=ydl.extract_info("https://www.youtube.com/watch?v={sID}".format(sID=id),download=False)['duration']
                player = vlc.MediaPlayer(info)
                # print(duration)
                player.play()
                time.sleep(duration)
                player.stop()
        elif(sys.argv[1]=="-s"):
            info=ydl.extract_info("ytsearch:%s lyrics" %" ".join(sys.argv[2:]),download=False)['entries'][0]['formats'][0]['url']
            id=ydl.extract_info("ytsearch:%s lyrics" %" ".join(sys.argv[2:]),download=False)['entries'][0]['id']
            duration=ydl.extract_info("https://www.youtube.com/watch?v={sID}".format(sID=id),download=False)['duration']
            player = vlc.MediaPlayer(info)
            # print(duration)
            player.play()
            time.sleep(duration)
        elif(sys.argv[1]=="-d"):
            ydl.extract_info("ytsearch:%s lyrics" %" ".join(sys.argv[2:]),download=True)['entries'][0]['formats'][0]['url']
        else:
            print("use -p for playlist\nuse -s for song\nuse -d to download song")

if __name__ == "__main__":

    t1 = threading.Thread(target=logToMDB)
    t2 = threading.Thread(target=play)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("done")
