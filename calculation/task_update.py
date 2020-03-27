import threading

class TaskUpdate:
    def __init__(self, interval, tick = None):
        self.stopped = False
        self.interval = interval
        self.tick = tick

    def update(self):
        if self.tick != None:
            self.tick()
        self.start()

    def start(self):
        if self.stopped == True:
            return
        self.timer = threading.Timer(self.interval, self.update)
        self.timer.start()

    def stop(self):
        if self.stopped == True:
            return
        self.stopped = True
        self.timer.cancel()
