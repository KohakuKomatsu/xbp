import ctypes
import os
import glob
import time
import threading
import random
import codecs
import sys

INTERVAL_SEC = 3


class BgSlider():
    def __init__(self):
        self.index = 0
        self.directory = None

    def setup(self):
        global off
        with codecs.open('path.txt', 'r', 'utf-8') as f:
            lines = f.readlines()
            self.directory = lines[0].strip()

    def worker(self):
        path = self.directory + r'\*.jpg'
        path.replace('\\\\', '\\')
        files = glob.glob(path)
        # [print(file) for file in files] # ファイルリストをコンソールにまとめて出力するときに使う
        # file = files[random.randint(0, len(files) - 1)] # ランダムにしたい場合はここを使う
        files = sorted(files) # 順番に表示したい場合はここを使う
        file = files[self.index] # 順番に表示したい場合はここを使う
        print(file)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, file, 0)
        if self.index == len(files) - 1:
            self.index = 0
        else:
            self.index += 1
        time.sleep(INTERVAL_SEC)

    def schedule(self, interval, f, wait=True):
        base_time = time.time()
        next_time = 0
        while True:
            try:
                t = threading.Thread(target=f)
                t.start()
                if wait:
                    t.join()
                next_time = ((base_time - time.time()) % interval) or interval
                time.sleep(next_time)
            except KeyboardInterrupt:
                exit()