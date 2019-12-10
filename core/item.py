from core.common import Item, View

class MountainItem(Item):
    def draw(self, view, **kwargs):
        ((x, y), (w, h)) = kwargs['xywh']
        padding = 2
        points = ((x + padding, y + h - padding), (x + w - padding, y + h - padding), (x + w // 2, y + padding))
        view.polygon(points, color=View.COLOR_BLACK, border=0)


class WaterItem(Item):
    def draw(self, view, **kwargs):
        ((x, y), (w, h)) = kwargs['xywh']
        padding = 2
        view.line((x + padding, y + h // 4), (x + w - padding, y + h // 4), color=View.COLOR_BLUE, border=1)
        view.line((x + padding, y + h // 2), (x + w - padding, y + h // 2), color=View.COLOR_BLUE, border=1)
        view.line((x + padding, y + h * 3 // 4), (x + w - padding, y + h * 3 // 4), color=View.COLOR_BLUE, border=1)


class BlockItem(Item):
    def draw(self, view, **kwargs):
        ((x, y), (w, h)) = kwargs['xywh']
        padding = 2
        view.rectangle(((x + padding, y + padding), (w - 2 * padding, h - 2 * padding)), color=View.COLOR_BLACK,
                       border=0)