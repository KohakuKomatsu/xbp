import ctypes
import os
import glob
import time
import threading
import random
import codecs
import sys

#importとはpythonでモジュールなどを利用するために使用するもの
INTERVAL_SEC = 3


class BgSlider():
    def __init__(self):
        self.index = 0
        self.directory = None

    def setup(self):
        global off
        with codecs.open('path.txt', 'r', 'utf-8') as f:
            #with構文は、close処理を省略することができる。開始時と終了時の定型処理を必ず実行してくれるというメリットがある。
            #asを使うことで、ライブラリ名に好きな名前をつけることができる。
            #path.txtというファイルを好きなディレクトリに書き換える。
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
          #pythonで条件分岐を行う際にif文を使用する
            self.index = 0
        else:
        #elseとは、条件式がFalseの場合行う処理
            self.index += 1
        time.sleep(INTERVAL_SEC)

    def schedule(self, interval, f, wait=True):
        base_time = time.time()
        next_time = 0
        while True:
            #while文は指定した条件式が真の間、処理を繰り返し実行。基本的な書式→while条件式：条件式が真の時に実行する文
            try:
                #tryは例外処理の基本で、その他にexcept
                t = threading.Thread(target=f)
                t.start()
                if wait:
                   #pythonで条件分岐を行う際にif文を使用する
                    t.join()
                next_time = ((base_time - time.time()) % interval) or interval
                time.sleep(next_time)
            except KeyboardInterrupt:
                #exceptは例外処理の基本で、その他にtryがある
                exit()
               


 if __name__ == "__main__":
    try:
        #tryは例外処理の基本で、その他にexcept
        bg = BgSlider()
        bg.setup()
        bg.schedule(INTERVAL_SEC, bg.worker, False)
    finally:
        #finallyは終了時に常に行う処理のこと
        ctypes.windll.user32.SystemParametersInfoW(20, 0, None, 0)