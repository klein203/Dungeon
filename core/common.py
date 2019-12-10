import uuid, random
from util.logger import Logger
import pygame

class Config(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Generic(object):
    SYS = -1
    SCENARIO = 0
    MAP = 1
    MONSTER = 2
    PLAYER = 3
    ITEM = 4

    def __init__(self, config):
        self.uuid = uuid.uuid4()
        self.name = config.name

    def __repr__(self):
        #         return "%s - %s" % (self.__class__.__name__, self.getName())
        return self.name

    def getUUID(self):
        return self.uuid

    def getName(self):
        return self.name


class Scenario(Generic):
    def __init__(self, modal, config):
        super().__init__(config)
        self.modal = modal

    def on_event(self, event):
        raise NotImplementedError("function on_event() should be implemented")

    def on_action(self):
        raise NotImplementedError("function on_action() should be implemented")

    def on_rendor(self, view):
        raise NotImplementedError("function on_rendor() should be implemented")

    def getModal(self):
        return self.modal


class Map(Generic):
    def __init__(self, scenario, config):
        super().__init__(config)
        self.scenario = scenario

    def getScenario(self):
        return self.scenario

    def draw(self, view, **kwargs):
        raise NotImplementedError("function draw() should be implemented")


class GameObject(Generic):
    def __init__(self, config):
        super().__init__(config)

        # position
        self.colIdx = -1
        self.rowIdx = -1

    def draw(self, view, **kwargs):
        raise NotImplementedError("function draw() should be implemented")

    def setPosIndex(self, colIdx, rowIdx):
        self.colIdx = colIdx
        self.rowIdx = rowIdx

    def getPosIndex(self):
        return self.colIdx, self.rowIdx


class Creature(GameObject):
    def __init__(self, scenario, config):
        super().__init__(config)
        self.scenario = scenario

        self.type = 0

        self.level = 1
        self.experience = 0

        #         self.str = 10
        #         self.dex = 10
        #         self.agi = 10
        #         self.int = 10
        #         self.con = 10
        #         self.luk = 10

        self.hp = 0
        #         self.sp = 0
        self.attack = 0
        self.defense = 0
        #         self.hit = 0
        #         self.avoid = 0

        # dice
        self.maxDice = 20

    def dice(self):
        return random.randint(1, self.maxDice)

    def move(self, dcol, drow):
        self.colIdx += dcol
        self.rowIdx += drow

    #     def moveToPos(self, rowIdx, colIdx):
    #         self.rowIdx = rowIdx
    #         self.colIdx = colIdx

    def reset(self):
        self.colIdx = 0
        self.rowIdx = 0

    def draw(self, view, **kwargs):
        super().draw(view, **kwargs)

    def getScenario(self):
        return self.scenario


class Item(GameObject):
    def __init__(self, config):
        super().__init__(config)
        self.blocked = config.blocked

    def draw(self, view, **kwargs):
        super().draw(view, **kwargs)

    def isBlock(self):
        return self.blocked


class PygModal(Generic):
    def __init__(self, config):
        super().__init__(config)
        pygame.init()
        self.running = False

        # all scenarios
        self.scenarios = dict()
        self.scenario = None

        self.view = None

    # def methodWrapper(appMethod):
    #     def m(*args, **kwargs):
    #         Logger.debug('begin %s' % appMethod)
    #         ret = appMethod(*args, **kwargs)
    #         Logger.debug('end %s, ret %s' % (appMethod, ret))
    #         return ret
    #
    #     return m

    def appendScenario(self, s):
        if isinstance(s, Scenario):
            self.scenarios[s.getName()] = s
        else:
            Logger.error('Error in loading scenario %s' % s)

    def setActiveScenario(self, name):
        if name in self.scenarios.keys():
            self.scenario = self.scenarios[name]
        else:
            Logger.error('Error in setting active scenario' % name)

    def getActiveScenario(self):
        return self.scenario

    def setView(self, view):
        self.view = view

    def getView(self):
        return self.view

    def getViewFPS(self):
        return self.view.getFPS()

    def viewTick(self):
        self.view.tick()

    def viewRender(self):
        # overall
        caption = "%s - FPS@%d" % (self.getName(), self.getViewFPS())
        pygame.display.set_caption(caption)

        # active scenario render
        self.getActiveScenario().on_render(self.getView())

        # view rendor
        self.getView().render()

    def run(self):
        self.running = True

        if self.getActiveScenario() == None:
            pygame.quit()
            return

        while self.running:
            self.viewTick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                self.getActiveScenario().on_event(event)

            #             self.getActiveScenario().on_action()

            self.viewRender()

        pygame.quit()


class View(Generic):
    COLOR_BLACK = (0, 0, 0)
    COLOR_WHITE = (255, 255, 255)
    COLOR_LIGHT_GREY = (191, 191, 191)
    COLOR_GREY = (127, 127, 127)
    COLOR_DARK_GREY = (63, 63, 63)
    COLOR_RED = (255, 0, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_BLUE = (0, 0, 255)

    def __init__(self, modal, config):
        super().__init__(config)
        self.modal = modal

        self.width = config.width
        self.height = config.height

        # clock tick and fps
        self.fps = config.fps
        self.clock = pygame.time.Clock()

        # font
        if pygame.font.get_init() == False:
            pygame.font.init()

        self.fontname = config.fontname
        self.fontsize = config.fontsize
        self.font = pygame.font.SysFont(self.fontname, self.fontsize, bold=False)

        # canvas
        self.canvas = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.canvas.get_size()).convert()
        self.background.fill(View.COLOR_WHITE)

    def getFPS(self):
        return self.clock.get_fps()

    def tick(self):
        return self.clock.tick_busy_loop(self.fps)

    def render(self):
        pygame.display.flip()
        self.canvas.blit(self.background, (0, 0))

    def rectangle(self, xywh, color, border=1):
        pygame.draw.rect(self.canvas, color, xywh, border)

    def line(self, start_xy, end_xy, color, border=1):
        pygame.draw.line(self.canvas, color, start_xy, end_xy, border)

    def circle(self, xy, r, color, border=0):
        pygame.draw.circle(self.canvas, color, xy, r, border)

    def polygon(self, points, color, border=0):
        #         points = (
        #             (137, 372),
        #             (232, 319),
        #             (383, 335)
        #         )
        pygame.draw.polygon(self.canvas, color, points, border)

    def text(self, xy, text, color, fontsize=None):
        if fontsize == None:
            surface = self.font.render(text, True, color)
        else:
            font = pygame.font.SysFont(self.fontname, fontsize, bold=False)
            surface = font.render(text, True, color)

        self.canvas.blit(surface, xy)