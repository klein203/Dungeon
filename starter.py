from util.logger import Logger
from delegator import GameDelegator


def main():
    Logger.setLevel(Logger.DEBUG)
    GameDelegator().run()


if __name__ == '__main__':
    main()