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
        ("\n""I don't like the way he's lookin' at you", 0.07),
        ("I'm startin' to think you want him, too", 0.07),
        ("Am I crazy? Have I lost ya?", 0.08),
        ("Even though I know you love me, can I help it?", 0.07),
        ("(Jealous, jealous, jealous)""\n", 0.05),
        ("I turn my chin music up", 0.08),
        ("And I'm puffin' my chest", 0.07),
        ("I'm gettin' red in the face", 0.07),
        ("You can call me obsessed", 0.06),
        ("It's not your fault that they hover", 0.06),
        ("I mean no disrespect", 0.09),
        ("It's my right to be hellish", 0.08),
        ("I still get jealous", 0.09),
    ]
    
    delays = [0.3, 5.4, 10.3, 12.9, 14.2, 15.2, 20.0, 23.0, 26.2, 28.0, 30.0, 33.0, 35.7,]
    
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