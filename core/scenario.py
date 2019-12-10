from core.common import View, Scenario, Map, Item
from util.logger import Logger
import pygame

class DefaultScenario(Scenario):
    def __init__(self, modal, config):
        super().__init__(modal, config)
        # constant
        self.MAP_PADDING_BLOCK = config.MAP_PADDING_BLOCK
        self.PADDING_BLOCK_PIXEL = config.PADDING_BLOCK_PIXEL
        self.CELL_PIXEL = config.CELL_PIXEL

        # slide window frame setting
        self.slideWindowCol = config.slideWindowCol
        self.slideWindowRow = config.slideWindowRow

        self.offsetCol = self.slideWindowCol // 2
        self.offsetRow = self.slideWindowRow // 2

        self.scrollColIdx = 0
        self.scrollRowIdx = 0

        # maps
        self.maps = dict()
        self.map = None

        # items
        self.items = []

        # players
        self.players = []
        self.player = None

        # monsters
        self.monsters = []

    # overwrite
    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.movePlayer(0, +1)
            elif event.key == pygame.K_LEFT:
                self.movePlayer(-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.movePlayer(+1, 0)
            elif event.key == pygame.K_UP:
                self.movePlayer(0, -1)

    def on_action(self):
        # dummy action
        pass

    def on_render(self, view):
        dx = self.MAP_PADDING_BLOCK * self.PADDING_BLOCK_PIXEL
        dy = self.MAP_PADDING_BLOCK * self.PADDING_BLOCK_PIXEL
        self.drawMap(view, dx, dy)
        #         self.drawItems(view, dx, dy)
        self.drawPlayer(view, dx, dy)

    #         self.drawText(view, dx, dy)

    # util functions
    def getCellPixel(self):
        return self.CELL_PIXEL

    ## map
    def getActiveMap(self):
        return self.map

    def getMapBorder(self):
        return self.getActiveMap().getBorder()

    ## slide window
    def getSlideWindowBorder(self):
        return (self.slideWindowCol, self.slideWindowRow)

    def getScrollIndex(self):
        return (self.scrollColIdx, self.scrollRowIdx)

    ## player
    def getPlayer(self):
        return self.player

    def getPlayerPosIndex(self):
        return self.getPlayer().getPosIndex()

    ## items
    def getItems(self):
        return self.items

    # reset functions
    def resetSlideIndex(self):
        self.scrollColIdx = 0
        self.scrollRowIdx = 0

    def reset(self):
        self.resetSlideIndex()
        self.player.reset()

    # init functions
    ## map
    def appendMap(self, m):
        if isinstance(m, Map):
            self.maps[m.getName()] = m
        else:
            Logger.error('Error in loading map %s' % m)

    def setActiveMap(self, name):
        if name in self.maps.keys():
            self.map = self.maps[name]

    ## player
    def setPlayer(self, p):
        self.player = p

    ## items
    def appendItem(self, item):
        if isinstance(item, Item):
            self.items[item.getName()] = item
        else:
            Logger.error('Error in loading item %s' % item)

    def setItems(self, items):
        self.items = items

    # logical action functions
    def movePlayer(self, dcol, drow):
        curColIdx, curRowIdx = self.getPlayerPosIndex()

        tryColIdx = curColIdx + dcol
        tryRowIdx = curRowIdx + drow

        mapBorderCol, mapBorderRow = self.getMapBorder()

        if tryColIdx >= 0 and tryColIdx < mapBorderCol and tryRowIdx >= 0 and tryRowIdx < mapBorderRow:
            if self.hasBlock(tryColIdx, tryRowIdx) == False:
                self.player.move(dcol, drow)
                self.updateScrollIndex()

    def hasBlock(self, colIdx, rowIdx):
        items = self.getActiveMap().getItems(colIdx, rowIdx)
        if items == None:
            return False

        for item in items:
            if item.isBlock():
                return True

        return False

    def updateScrollIndex(self):
        curColIdx, curRowIdx = self.getPlayerPosIndex()
        mapBorderCol, mapBorderRow = self.getMapBorder()

        if curColIdx < self.offsetCol:
            self.scrollColIdx = 0
        elif curColIdx < mapBorderCol - self.slideWindowCol + self.offsetCol:
            self.scrollColIdx = curColIdx - self.offsetCol + 1
        else:
            self.scrollColIdx = mapBorderCol - self.slideWindowCol

        if curRowIdx < self.offsetRow:
            self.scrollRowIdx = 0
        elif curRowIdx < mapBorderRow - self.slideWindowRow + self.offsetRow:
            self.scrollRowIdx = curRowIdx - self.offsetRow + 1
        else:
            self.scrollRowIdx = mapBorderRow - self.slideWindowRow

    # rendor functions
    def convertToSlideWindowPos(self, colIdx, rowIdx):
        sColIdx = self.offsetCol - 1
        sRowIdx = self.offsetRow - 1

        mapBorderCol, mapBorderRow = self.getMapBorder()

        if colIdx < self.offsetCol:
            sColIdx = colIdx
        elif colIdx > mapBorderCol - (self.slideWindowCol - self.offsetCol) - 1:
            sColIdx = colIdx - (mapBorderCol - self.slideWindowCol)

        if rowIdx < self.offsetRow:
            sRowIdx = rowIdx
        elif rowIdx > mapBorderRow - (self.slideWindowRow - self.offsetRow) - 1:
            sRowIdx = rowIdx - (mapBorderRow - self.slideWindowRow)

        return (sColIdx, sRowIdx)

    def drawMap(self, view, dx, dy):
        cellPixel = self.getCellPixel()

        # slide window frame
        x = dx
        y = dy
        w = self.slideWindowCol * cellPixel
        h = self.slideWindowRow * cellPixel
        self.getActiveMap().draw(view, **{'xywh': ((x, y), (w, h))})

    def drawItems(self, view, dx, dy):
        cellPixel = self.getCellPixel()

        # items in cells
        for i in range(self.slideWindowRow):
            for j in range(self.slideWindowCol):
                sColIdx = j + self.scrollColIdx
                sRowIdx = i + self.scrollRowIdx
                if self.hasBlock(sColIdx, sRowIdx):
                    pad = 2
                    x = dx + j * cellPixel + pad
                    y = dy + i * cellPixel + pad
                    w = cellPixel - 2 * pad
                    h = w
                    # TODO

                    view.rectangle(((x, y), (w, h)), color=View.COLOR_BLACK, border=0)

    def drawPlayer(self, view, dx, dy):
        cellPixel = self.getCellPixel()
        (curColIdx, curRowIdx) = self.getPlayerPosIndex()
        (slideColIdx, slideRowIdx) = self.convertToSlideWindowPos(curColIdx, curRowIdx)
        pad = 3
        x = dx + slideColIdx * cellPixel + pad
        y = dy + slideRowIdx * cellPixel + pad
        w = cellPixel - 2 * pad
        h = w
        self.getPlayer().draw(view, **{'xywh': ((x, y), (w, h))})

    def drawText(self, view, dx, dy):
        cellPixel = self.getCellPixel()

        # map border
        view.text((dx + (cellPixel - view.fontsize) // 2,
                   dy + self.slideWindowRow * cellPixel + (cellPixel - view.fontsize) // 2),
                  text="slide (r%d x c%d)" % self.getSlideWindowBorder(),
                  color=View.COLOR_BLACK)

        view.text((dx + (cellPixel - view.fontsize) // 2,
                   dy + self.slideWindowRow * cellPixel + (cellPixel - view.fontsize) // 2),
                  text="map (r%d x c%d)" % self.getMapBorder(),
                  color=View.COLOR_BLACK)

# class BattleScenario(Scenario):
#     def __init__(self, modal, config):
#         super().__init__(modal, config)

#     def battle(self, attacker, defencer):
#         pass
