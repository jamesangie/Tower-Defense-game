from ADP import *


def testEnemyMoving():
    m = Map(1, [(1, 1),(1, 2),(1, 3),(1, 4)])
    enemy = Enemy("enemy1", m.route[0][0], m.route[0][1])
    print("pos of enemy: " + str(enemy.get_pos()) )
    enemy.move(m)
    print("pos of enemy after moving 1 time: " + str(enemy.get_pos()))


def testMapRouteExtend():
    m = Map(1, [(1, 1)])
    print("Route of m: " + str(m.route))
    m.extend_route((2, 2))
    print("Route of m after Extend to (2, 2): " + str(m.route))
    m.extend_route((-10, -10))
    print("Route of m after Extend to (-10, -10): " + str(m.route))
    m.extend_route((-9, -9))
    print("Route of m after Extend to (-9, -9): " + str(m.route))
    m.extend_route((-9, -9))
    print("Route of m after Extend to (-9, -9): " + str(m.route))
    mm = Map(1, [(1, 1)])
    mm.extend_route((7, 3))
    print("Route of mm after Extend to (7, 3): " + str(mm.route))
    mm.extend_route((9, 9))
    print("Route of mm after Extend to (9, 9): " + str(mm.route))


testMapRouteExtend()
