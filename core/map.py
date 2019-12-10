import random
from core.common import Map, Config, View
from core.item import MountainItem, WaterItem

mountainItemConfig = {
    'name': 'mountain',
    'blocked': True
}

waterItemConfig = {
    'name': 'water',
    'blocked': False
}

class DefaultMap(Map):
    def __init__(self, scenario, config):
        super().__init__(scenario, config)

        self.col = config.col
        self.row = config.row
        self.board = [[None for j in range(self.col)] for i in range(self.row)]

        self.randomMode = config.randomMode
        self.p = config.p

        if self.randomMode:
            self.randomMap(self.p)

    def getBorder(self):
        return self.col, self.row

    def getItems(self, colIdx, rowIdx):
        return self.board[rowIdx][colIdx]

    def appendItem(self, item, colIdx, rowIdx):
        if self.board[rowIdx][colIdx] == None:
            self.board[rowIdx][colIdx] = list()
        self.board[rowIdx][colIdx].append(item)

    def randomMap(self, p=0.999):
        items_class = [MountainItem, WaterItem]

        items_config = [mountainItemConfig, waterItemConfig]
        for i in range(self.row):
            for j in range(self.col):
                if random.random() > p:
                    idx = random.randint(0, len(items_class) - 1)
                    clazz = items_class[idx]
                    item = clazz(Config(**items_config[idx]))
                    item.setPosIndex(j, i)
                    self.appendItem(item, j, i)

    def randomMountainMap(self, p=0.999):
        for i in range(self.row):
            for j in range(self.col):
                if random.random() > p:
                    item = MountainItem(Config(**mountainItemConfig))
                    item.setPosIndex(j, i)
                    self.appendItem(item, j, i)

    def draw(self, view, **kwargs):
        ((x, y), (w, h)) = kwargs['xywh']
        view.rectangle(((x, y), (w, h)), color=View.COLOR_BLACK, border=1)

        (slideWindowCol, slideWindowRow) = self.getScenario().getSlideWindowBorder()
        (scrollColIdx, scrollRowIdx) = self.getScenario().getScrollIndex()
        cellPixel = self.getScenario().getCellPixel()

        # grid
        #         for j in range(1, slideWindowCol):
        #             start_x = dx + j * cellPixel
        #             start_y = dy
        #             end_x = start_x
        #             end_y = start_y + slideWindowRow * cellPixel
        #             view.line((start_x, start_y), (end_x, end_y), color=View.COLOR_LIGHT_GREY, border=1)

        #         for i in range(1, slideWindowRow):
        #             start_x = dx
        #             start_y = dy + i * cellPixel
        #             end_x = start_x + slideWindowCol * cellPixel
        #             end_y = start_y
        #             view.line((start_x, start_y), (end_x, end_y), color=View.COLOR_LIGHT_GREY, border=1)

        # items on map layer
        for i in range(slideWindowRow):
            for j in range(slideWindowCol):
                items = self.board[scrollRowIdx + i][scrollColIdx + j]
                if items != None:
                    for item in items:
                        c_x = x + j * cellPixel
                        c_y = y + i * cellPixel
                        item.draw(view, **{'xywh': ((c_x, c_y), (cellPixel, cellPixel))})