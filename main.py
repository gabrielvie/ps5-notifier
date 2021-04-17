import time
import colored

from ps5_notifier import Notifier, Scrapper


def loop(stopped, scrapper):
    while not stopped.wait(60.0):
        scrapper.proccess()


if __name__ == "__main__":
    notifier = Notifier()
    scrapper = Scrapper(notifier=notifier)

    print("%sStarting...%s" % (colored.fg(11), colored.attr(0)))

    while True:
        try:
            scrapper.process()
        except Exception as exception:
            print(exception.__str__)
        time.sleep(300)
