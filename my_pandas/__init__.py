import threading
import time


def a():
    for i in range(5):
        time.sleep(0.5)
    print('aaa')


def b():
    print('bbb')


thread = threading.Thread(target=a)
thread.start()

b()
