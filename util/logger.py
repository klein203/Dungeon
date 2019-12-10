class Logger(object):
    level = 0

    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    FATAL = 4

    DICT = {
        DEBUG: 'D',
        INFO: 'I',
        WARNING: 'W',
        ERROR: 'E',
        FATAL: 'F'
    }

    @staticmethod
    def setLevel(level):
        Logger.level = level

    @staticmethod
    def log(message, level):
        if level >= Logger.level:
            print('[%s] %s' % (Logger.DICT[level], message))

    @staticmethod
    def debug(message):
        Logger.log(message, level=Logger.DEBUG)

    @staticmethod
    def info(message):
        Logger.log(message, level=Logger.INFO)

    @staticmethod
    def warning(message):
        Logger.log(message, level=Logger.WARNING)

    @staticmethod
    def error(message):
        Logger.log(message, level=Logger.ERROR)

    @staticmethod
    def fatal(message):
        Logger.log(message, level=Logger.FATAL)
