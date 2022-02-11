import sys


class Logger(object):

    def __init__(self, today_folder):
        self.terminal = sys.stdout
        filename = F"{today_folder}logger.log"
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
