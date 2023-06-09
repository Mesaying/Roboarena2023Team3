from enum import Enum


class WeaponTyp(Enum):
    hitscan = "hitscan"
    projectile = "projectile"

class WeaponName(Enum):
    basicHitscan = "basicHitscan"


class Weapon:
    def __init__(self, name : WeaponName) -> None:
        self.damage = 0
        self.size = 0
        self.typ = WeaponTyp.hitscan
        self.name = name
        self.getWeaponStats(name)
        self.ticksToNextShoot = 10

    def getWeaponStats(self, name : WeaponName) -> None:
        self.damage = 0
        self.size = 0
        match(name):
            case WeaponName.basicHitscan:
                self.damage = 10
                self.size = 1000
                self.typ = WeaponTyp.hitscan
    
    # hit or not hit
    def shootWeapon(self) -> bool:
        pass