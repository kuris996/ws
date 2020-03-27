import threading

class TaskUpdate:
    def __init__(self, app, interval, tick = None):
        self.__stopped = False
        self.__interval = interval
        self.__tick = tick
        self.__app = app

    def __update(self):
        if self.__tick != None:
            self.__tick(self.__app)
        self.start()

    def start(self):
        if self.__stopped == True:
            return
        self.__timer = threading.Timer(self.__interval, self.__update)
        self.__timer.start()

    def stop(self):
        if self.__stopped == True:
            return
        self.__stopped = True
        self.__timer.cancel()
