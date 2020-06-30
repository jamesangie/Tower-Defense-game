from ADP import *


def testMapRouteExtend():
    m = Map("map1", (1, 1))
    print("Route of m: " + str(m.route))
    m.extend_route((2, 2))
    print("Route of m after Extend to (2, 2): " + str(m.route))
    m.extend_route((-10, -10))
    print("Route of m after Extend to (-10, -10): " + str(m.route))
    m.extend_route((-9, -9))
    print("Route of m after Extend to (-9, -9): " + str(m.route))
    m.extend_route((-9, -9))
    print("Route of m after Extend to (-9, -9): " + str(m.route))
    mm = Map("map1", (1, 1))
    mm.extend_route((7, 3))
    print("Route of mm after Extend to (7, 3): " + str(mm.route))
    mm.extend_route((9, 9))
    print("Route of mm after Extend to (9, 9): " + str(mm.route))


def testEnemyMoving():
    m = Map("map1", (1, 1))
    m.extend_route((7, 3))
    enemy = Enemy("enemy1", m.route[0][0], m.route[0][1])
    print("pos of enemy: " + str(enemy.get_pos()))
    enemy.move(m)
    print("pos of enemy after moving 1 time: " + str(enemy.get_pos()))


def testInitializeStatsFile():
    initialize_stats()
    with open(os.path.join(stats_path, "object_stats"), 'r') as fhs:
        s = fhs.read()
        stats = json.loads(s)
    print("Default stats file format: "+str(stats))


def testUpdateRoute():
    initialize_stats()
    updateRoute("map1", [(1, 1), (2, 2), (3, 3)])
    with open(os.path.join(stats_path, "object_stats"), 'r') as fhs:
        s = fhs.read()
        stats = json.loads(s)
    print("new route: "+str(stats["map"]["map1"]["route"]))


def testMapMakeRoute():
    initialize_stats()
    m = Map("map1")
    print(m.route)
    m.makeRoute()

testInitializeStatsFile()
#testUpdateRoute()
testMapMakeRoute()
#testMapRouteExtend()
