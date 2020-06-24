from ADP import *

def testEnemyMoving():
    m = Map(1, [(1, 1),(1, 2),(1, 3),(1, 4)])
    enemy = Enemy("enemy1", m.route[0][0], m.route[0][1])
    print("pos of enemy: " + str(enemy.get_pos()) )
    enemy.move(m)
    print("pos of enemy after moving 1 time: " + str(enemy.get_pos()))

def testMapRouteExtend():
    m = Map(1, [(1, 1)])
    print("Route of map: " + str(m.route))
    m.extend_route((2,2))
    print("Route after Extend to (2, 2): " + str(m.route))
    m.extend_route((-10, -10))
    print("Route after Extend to (-10, -10): " + str(m.route))


testMapRouteExtend()