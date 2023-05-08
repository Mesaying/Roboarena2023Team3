class terrain:
    def __init__(self):
        self.movement
        self.solid
        self.damage
        self.type


class water(
    terrain
):  # inherits from the motherclass terrain and gets the attributes from terrain
    movement = (
        0.5  # multiplicator how fast the robot move through this terrain
    )
    solid = 0  # if the robot can move through this terrain(0=passable, 1= not passable)
    damage = 0  # how much damage the robot takes when passing through
    type = "a"


class fire(terrain):
    movement = 1.0
    solid = 0
    damage = 10
    type = "f"


class spikes(terrain):
    movement = 1.0
    solid = 0
    damage = 20
    type = "s"


class wall(terrain):
    movement = 0
    solid = 1
    damage = 0
    type = "w"


class boost(terrain):
    movement = 2.0
    solid = 0
    damage = 0
    type = "b"


class normal(terrain):
    movement = 1.0
    solid = 0
    damage = 0
    type = "n"


test_tyle = water()
print(test_tyle.movement)
print(test_tyle.solid)
print(test_tyle.damage)
print(test_tyle.type)
