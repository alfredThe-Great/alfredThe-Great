import time
from threading import Thread, Lock
import sys

lock = Lock()

def animate_text(text, delay=0.1):
    with lock:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

def sing_lyric(lyric, delay, speed):
    time.sleep(delay)
    animate_text(lyric, speed)

def sing_song():
    lyrics = [
        ("\n""Before I make a move", 0.09),
        ("(Ooh-ooh-ooh-ooh-ooh)", 0.11),
        ("So baby, come light me up", 0.07),
        ("And maybe I'll let you on it", 0.07),
        ("A little bit dangerous", 0.07),
        ("But baby, that's how I want it", 0.07),
        ("A little less conversation, and", 0.06),
        ("A little more touch my body", 0.08),
        ("'Cause I'm so into you, into you, into you", 0.10),
    ]
    
    delays = [0.3, 2.7, 5.4, 8.0, 10.0, 12.4, 14.0, 15.5, 19.0,]
    
    threads = []
    for i in range(len(lyrics)):
        lyric, speed = lyrics[i]
        t = Thread(target=sing_lyric, args=(lyric, delays[i], speed))
        threads.append(t)
        t.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    sing_song()