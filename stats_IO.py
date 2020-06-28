import os
import json

# globel variables
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'image')
stats_path = os.path.join(current_path, "STATS")


# Initialize a new stats file
def initialize_stats():
    """
    clear all the info in the stats file
    :return: None
    """
    d = {"tower": {"tower1": {"cost": 50, "ATT": 2, "attack_speed": 2, "range": 180, "img": "tower/tower1.jpg"}},
         "enemy": {"enemy1": {"speed": 20, "hp": 100, "gold_drop": 25, "img": "enemy/enemy1.jpg"}},
         "map": {"map1":{"route": [], "img": "map/map1.jpg"}, "map2": {"route": [], "img": "map/map2.jpg"}}}
    with open(os.path.join(stats_path, "object_stats"), 'w') as fhl:
        s1 = json.dumps(d)
        fhl.write(s1)


# Save a new Tower with stats into the stats file
def saveNewTower(name, cost, ATT, attack_speed, att_range, img):
    """
    Save the new Tower with stats into the stats file
    :return: None
    """
    with open(os.path.join(stats_path, "object_stats"), 'r') as fhs:
        s = fhs.read()
        stats = json.loads(s)
    stats["tower"][name] = {"cost": cost, "ATT": ATT, "attack_speed": attack_speed, "range": att_range, "img": img}
    with open(os.path.join(stats_path, "object_stats"), 'w') as fhl:
        s1 = json.dumps(stats)
        fhl.write(s1)


# Save a new Enemy with stats into the stats file
def saveNewEnemy(name, speed, hp, gold_drop):
    with open(os.path.join(stats_path, "object_stats"), 'r') as fhs:
        s = fhs.read()
        stats = json.loads(s)
    stats["enemy"][name] = {"speed": speed, "hp": hp, "gold_drop": gold_drop}
    with open(os.path.join(stats_path, "object_stats"), 'w') as fhl:
        s1 = json.dumps(stats)
        fhl.write(s1)


def updateRoute(map_name, route):
    with open(os.path.join(stats_path, "object_stats"), 'r') as fhs:
        s = fhs.read()
        stats = json.loads(s)
    stats["map"][map_name]["route"] = route


# Read stats of all the towers
def readTower():
    with open(os.path.join(stats_path, "object_stats"), 'r') as fhs:
        s = fhs.read()
        stats = json.loads(s)
    return stats["tower"]


# Read stats of all the enemies
def readEnemy():
    with open(os.path.join(stats_path, "object_stats"), 'r') as fhs:
        s = fhs.read()
        stats = json.loads(s)
    return stats["enemy"]


# Read stats of the map
def readMap():
    with open(os.path.join(stats_path, "object_stats"), 'r') as fhs:
        s = fhs.read()
        stats = json.loads(s)
    return stats["map"]
