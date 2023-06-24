from enum import Enum


class WeaponTyp(Enum):
    hitscan = "hitscan"
    projectile = "projectile"


class WeaponName(Enum):
    basicHitscan = "basicHitscan"
    basicLaser = "basicLaser"
    strongLaser = "strongLaser"
    sniper = "sniper"


class Weapon:
    def __init__(self, name: WeaponName) -> None:
        self.damage = 0
        self.size = 0
        self.ticksToNextShoot = 10
        self.typ = WeaponTyp.hitscan
        self.name = name
        self.getWeaponStats(name)

    def getWeaponStats(self, name: WeaponName) -> None:
        match (name):
            case WeaponName.basicHitscan:
                self.damage = 10
                self.size = 1000
                self.ticksToNextShoot = 4
                self.typ = WeaponTyp.hitscan
            case WeaponName.basicLaser:
                self.damage = 3
                self.size = 400
                self.ticksToNextShoot = 0
                self.typ = WeaponTyp.hitscan
            case WeaponName.strongLaser:
                self.damage = 7
                self.size = 200
                self.ticksToNextShoot = 0
                self.typ = WeaponTyp.hitscan
            case WeaponName.sniper:
                self.damage = 50
                self.size = 2000
                self.ticksToNextShoot = 15
                self.typ = WeaponTyp.hitscan
