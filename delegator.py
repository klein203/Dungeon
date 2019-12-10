from core.common import PygModal, Config
from core.view import DefaultView
from core.map import DefaultMap
from core.scenario import DefaultScenario
from core.creature import Player

defaultGlobalConfig = {
    'name': 'DND'
}

defaultViewConfig = {
    'name': '400x300',
    'width': 400,
    'height': 300,
    'fps': 50,

    #     'fontname': 'arial',
    'fontname': 'calibri',
    'fontsize': 10
}

defaultScenarioConfig = {
    'name': 'default_scenario',

    'CELL_PIXEL': 20,
    'MAP_PADDING_BLOCK': 2,
    'PADDING_BLOCK_PIXEL': 30,

    'slideWindowRow': 10,
    'slideWindowCol': 15
}

defaultMapConfig = {
    'name': 'default_map',
    'row': 15,
    'col': 20,
    'randomMode': True,
    'p': 0.98
}

# player
defaultPlayerConfig = {
    'name': 'Hero'
}

warriorPlayerConfig = {
    'name': 'Warrior'
}

# items
defaultItemConfig = {
    'name': 'Item',
    'blocked': False
}

# mountainItemConfig = {
#     'name': 'mountain',
#     'blocked': True
# }
#
# waterItemConfig = {
#     'name': 'water',
#     'blocked': False
# }

class GameDelegator(object):
    def __init__(self):
        # init modal
        modal = PygModal(Config(**defaultGlobalConfig))

        # init scenario
        scen = DefaultScenario(modal, Config(**defaultScenarioConfig))

        # append scenario
        modal.appendScenario(scen)
        modal.setActiveScenario(scen.getName())

        # init map
        mp = DefaultMap(scen, Config(**defaultMapConfig))
        scen.appendMap(mp)
        scen.setActiveMap(mp.getName())

        # bind items to map
        #         items = Magic.genMountainItems(mp.getBorder(), n=3)
        #         for item in items:
        #             colIdx, rowIdx = item.getPosIndex()
        #             mp.appendItem(item, colIdx, rowIdx)

        # append player
        ply = Player(scen, Config(**defaultPlayerConfig))
        scen.setPlayer(ply)

        # bind view
        vw = DefaultView(modal, Config(**defaultViewConfig))
        modal.setView(vw)

        self.modal = modal

    def run(self):
        self.modal.run()