from core.common import Config
from core.map import DefaultMap
from core.scenario import DefaultScenario
from core.creature import Player

# testGlobalConfig = {
#     'name': 'test_case'
# }

# testViewConfig = {
#     'name': 'test_400x300',
#     'width': 400,
#     'height': 300,
#     'fps': 50
# }

testScenarioConfig = {
    'name': 'test_scenario',

    'CELL_PIXEL': 15,
    'MAP_PADDING_BLOCK': 2,
    'PADDING_BLOCK_PIXEL': 20,
    
    'slideWindowRow': 7,
    'slideWindowCol': 11
}

testMapConfig = {
    'name': 'test_map',
    'row': 12,
    'col': 16,
    'randomMode': True,
    'p': 0.98
}

testPlayerConfig = {
    'name': 'DummyPlayer'
}

    
def testMovePlayerOnDefaultScenario():
    scen = DefaultScenario(None, Config(**testScenarioConfig))

    mp = DefaultMap(scen, Config(**testMapConfig))
    scen.appendMap(mp)
    scen.setActiveMap(mp.getName())

    ply = Player(scen, Config(**testPlayerConfig))
    scen.setPlayer(ply)

    print("Testing movePlayer and scrollMap...", end="")
    assert(scen.getMapBorder() == (16, 12))
    assert(scen.getSlideWindowBorder() == (11, 7))
    
    assert(scen.getPlayerPosIndex() == (0, 0))
    assert(scen.getScrollIndex() == (0, 0))
    scen.movePlayer(+4, 0)
    assert(scen.getPlayerPosIndex() == (4, 0))
    assert(scen.getScrollIndex() == (0, 0))
    scen.movePlayer(+1, 0)
    assert(scen.getPlayerPosIndex() == (5, 0))
    assert(scen.getScrollIndex() == (1, 0))
    scen.movePlayer(+4, 0)
    assert(scen.getPlayerPosIndex() == (9, 0))
    assert(scen.getScrollIndex() == (5, 0))
    scen.movePlayer(+1, 0)
    assert(scen.getPlayerPosIndex() == (10, 0))
    assert(scen.getScrollIndex() == (5, 0))
    scen.movePlayer(+5, 0)
    assert(scen.getPlayerPosIndex() == (15, 0))
    assert(scen.getScrollIndex() == (5, 0))
    
    scen.movePlayer(0, +2)
    assert(scen.getPlayerPosIndex() == (15, 2))
    assert(scen.getScrollIndex() == (5, 0))
    scen.movePlayer(0, +1)
    assert(scen.getPlayerPosIndex() == (15, 3))
    assert(scen.getScrollIndex() == (5, 1))
    scen.movePlayer(0, +4)
    assert(scen.getPlayerPosIndex() == (15, 7))
    assert(scen.getScrollIndex() == (5, 5))
    scen.movePlayer(0, +1)
    assert(scen.getPlayerPosIndex() == (15, 8))
    assert(scen.getScrollIndex() == (5, 5))
    scen.movePlayer(0, +3)
    assert(scen.getPlayerPosIndex() == (15, 11))
    assert(scen.getScrollIndex() == (5, 5))
    
    print("Pass!")

def testConvertToSlideWindowPosOnDefaultScenario():
    scen = DefaultScenario(None, Config(**testScenarioConfig))

    mp = DefaultMap(scen, Config(**testMapConfig))
    scen.appendMap(mp)
    scen.setActiveMap(mp.getName())

    ply = Player(scen, Config(**testPlayerConfig))
    scen.setPlayer(ply)

    print("Testing convertToSlideWindowPos...", end="")
    assert(scen.getMapBorder() == (16, 12))
    assert(scen.getSlideWindowBorder() == (11, 7))
    
    assert(scen.convertToSlideWindowPos(0, 0) == (0, 0))
    assert(scen.convertToSlideWindowPos(3, 0) == (3, 0))
    assert(scen.convertToSlideWindowPos(4, 0) == (4, 0))
    assert(scen.convertToSlideWindowPos(9, 0) == (4, 0))
    assert(scen.convertToSlideWindowPos(10, 0) == (5, 0))
    assert(scen.convertToSlideWindowPos(15, 0) == (10, 0))
    
    assert(scen.convertToSlideWindowPos(0, 1) == (0, 1))
    assert(scen.convertToSlideWindowPos(0, 2) == (0, 2))
    assert(scen.convertToSlideWindowPos(0, 7) == (0, 2))
    assert(scen.convertToSlideWindowPos(0, 8) == (0, 3))
    assert(scen.convertToSlideWindowPos(0, 11) == (0, 6))
    
    assert(scen.convertToSlideWindowPos(15, 11) == (10, 6))
    
    print("Pass!")

def testAll():
    testConvertToSlideWindowPosOnDefaultScenario()
    testMovePlayerOnDefaultScenario()


