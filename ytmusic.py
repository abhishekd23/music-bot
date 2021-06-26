import datetime
import vlc,time
import threading
from youtube_dl import YoutubeDL 
import sys, os
import pymongo
#Logging into MongoDb
def logToMDB():
    client = pymongo.MongoClient("mongodb+srv://admin:test@cluster0.mikev.mongodb.net/history?retryWrites=true&w=majority")
    db = client.history.collection1
    logval = {
        "user name": os.getlogin(),
      "song title": "{}".format(sys.argv[1]),
      "time": datetime.datetime.now()
    }

    db.insert_one(logval)

#Function to play song
def play():
    ydl_opts = {
        'writesubtitles': False,
        'format': 'mp4',
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
            player.stop()
        else:
            print("use -p for playlist\n use -s for song")

if __name__ == "__main__":

    # n = sys.argv[1]
    # # t1 = threading.Thread(target=logToMDB)
    # t2 = threading.Thread(target=play)

    # # t1.start()
    # t2.start()
    # # t1.join()
    # t2.join()
    # print("done")
    play()
    print("done")