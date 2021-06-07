class Tower:

    def __init__(self, x, origin, destination, auxiliary):
        self.x = x
        self.origin = origin
        self.destination = destination
        self.auxiliary = auxiliary


__move_set = []


def __move_disks(tower):
    if not tower.x == 1:
        __move_disks(Tower(tower.x - 1, tower.origin, tower.auxiliary, tower.destination))
        __move_set.append((tower.x, tower.destination))
        __move_disks(Tower(tower.x - 1, tower.auxiliary, tower.destination, tower.origin))
        return
    __move_set.append((tower.x, tower.destination))


def solve(number_of_disks):
    __move_disks(Tower(number_of_disks, 1, 3, 2))
    return __move_set


for n in solve(7):
    print(n)
