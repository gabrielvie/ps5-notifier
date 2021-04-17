import time
import colored

from ps5_notifier import Notifier, Scrapper

if __name__ == "__main__":
    notifier = Notifier()
    scrapper = Scrapper(notifier=notifier)

    print("%sStarting...%s" % (colored.fg(11), colored.attr(0)))

    while True:
        try:
            scrapper.process()
        except Exception as exception:
            print(exception.__str__)

        # TODO: provide this value with cli argument
        time.sleep(300)
