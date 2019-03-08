"""
threading module demo
"""
import threading, time, shutil, os


def loop():
    print('thread {} is running '.format(threading.current_thread().name))
    n = 0
    while n < 10:
        n += 1
        print('thread {} run no.{}'.format(threading.current_thread().name, n))
        time.sleep(0.5)
    print('thread {} is over'.format(threading.current_thread().name))


def copyfile(source, destination):
    """
    :return:
    """

    shutil.copy(source, destination)


if __name__ == '__main__':
    t = threading.Thread(target=loop, name='loop')
    t.start()
    t.join()
