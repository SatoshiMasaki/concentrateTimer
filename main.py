import time
import ctypes
import threading
import pygame
from mutagen.mp3 import MP3 as mp3
import re
import sys

SECOND = 60
MINUTES = 25


def sound():
    sound_path = "decision1.mp3"
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play(1)
    time.sleep(mp3(sound_path).info.length)
    pygame.mixer.music.stop()
    time.sleep(1)


def explain():
    print("----------------------")
    print("操作方法")
    print("「+」 : 時間を5秒延長する")
    print("「-」 : 時間を5秒短縮する")
    print("----------------------")


class Timer:
    def __init__(self, repeat_count):
        self.remaining_time = 0
        self.pattern_plus = re.compile("\+")
        self.pattern_minus = re.compile("\-")
        self.repeat_count = repeat_count

    def timer_controller(self):
        for count in range(self.repeat_count):
            print("{} 週目 : ".format(count + 1))
            self.screan_lock(5)
            self.count_down()

    def screan_lock(self, rest_time: int):
        start = time.time()
        remind_flag = True
        while time.time() - start < SECOND * rest_time:
            if time.time() - start > SECOND * 3 and remind_flag:
                sound()
                remind_flag = False
            ctypes.windll.user32.LockWorkStation()
        sound()

    def count_down(self):
        self.remaining_time = MINUTES * SECOND
        while True:
            if self.remaining_time <= 0:
                break
            time.sleep(1)
            self.remaining_time -= 1
        sound()

    def display_time(self):
        try:
            while True:
                input_key = input()
                if input_key == "":
                    minitus = self.remaining_time // SECOND
                    second = self.remaining_time % SECOND
                    print("残り時間 : {}分{}秒".format(minitus, second))
                elif self.pattern_plus.match(input_key):
                    self.remaining_time += 5 * len(input_key)
                    minitus = self.remaining_time // SECOND
                    second = self.remaining_time % SECOND
                    print("残り時間 : {}分{}秒".format(minitus, second))
                elif self.pattern_minus.match(input_key):
                    self.remaining_time -= 5 * len(input_key)
                    minitus = self.remaining_time // SECOND
                    second = self.remaining_time % SECOND
                    print("残り時間 : {}分{}秒".format(minitus, second))
        except KeyboardInterrupt:
            sys.exit()
        

if __name__ == '__main__':
    if len(sys.argv) == 1:
        repeat_count = None
        while True:
            try:
                repeat_count = input("繰り返しの回数を入力してください : ")
                if int(repeat_count) > 0:
                    break
            except ValueError as e:
                print("再入力してください")
    else:
        repeat_count = int(sys.argv[1])

    print("{} 回繰り返します".format(repeat_count))
    explain()
    timer = Timer(int(repeat_count))
    count_down_thread = threading.Thread(target=timer.timer_controller)
    display_time_thread = threading.Thread(target=timer.display_time)
    count_down_thread.setDaemon(True)
    count_down_thread.start()
    display_time_thread.setDaemon(True)
    display_time_thread.start()

    count_down_thread.join()
    sys.exit()

