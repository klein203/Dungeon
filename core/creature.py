from core.common import Creature, View

class Player(Creature):
    def __init__(self, scenario, config):
        super().__init__(scenario, config)
        self.setPosIndex(0, 0)

    def draw(self, view, **kwargs):
        ((x, y), (w, h)) = kwargs['xywh']
        padding = 2
        # draw body
        points = ((x + padding, y + h - padding), (x + w - padding, y + h - padding), (x + w // 2, y + padding))
        view.polygon(points, color=View.COLOR_GREY, border=0)
        # draw head
        view.circle((x + w // 2, y + h // 3), h * 5 // 12, color=View.COLOR_GREY, border=0)

        # debug


#         offset = self.getScenario().getCellPixel()
#         view.text((x + offset, y),
#                   text='(%d, %d)' % (self.colIdx, self.rowIdx),
#                   color=View.COLOR_GREY)


class Monster(Creature):
    def draw(self, view, **kwargs):
        super().draw(view, **kwargs)


class SlimeMonster(Monster):
    def draw(self, view, **kwargs):
        ((x, y), (w, h)) = kwargs['xywh']
        padding = 2
        #         view.circle((x + w // 2, y + h // 2), w // 2 - padding, color=View.COLOR_DARK_GREY, border=0)
        #         view.line((x + w // 2, y + padding), (x + w // 2, y + h - padding), color=View.COLOR_DARK_GREY, border=1)
        #         view.line((x + padding, y + h // 2), (x + w - padding, y + h // 2), color=View.COLOR_DARK_GREY, border=1)
        view.text((x + w // 2, y + h // 2), text="slime", color=View.COLOR_BLUE)


class ShinyMonster(Monster):
    def draw(self, view, **kwargs):
        ((x, y), (w, h)) = kwargs['xywh']
        padding = 2
        view.circle((x + w // 2, y + h // 2), w // 2 - padding, color=View.COLOR_DARK_GREY, border=0)
        view.line((x + w // 2, y + padding), (x + w // 2, y + h - padding), color=View.COLOR_DARK_GREY, border=1)
        view.line((x + padding, y + h // 2), (x + w - padding, y + h // 2), color=View.COLOR_DARK_GREY, border=1)