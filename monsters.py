class Entity:
    def __init__(self, name: str, health_max: int, attack: int, defense: int) -> None:
        self.name = name
        self.health_max = health_max
        self.health = health_max
        self.attack = attack
        self.defense = defense
    
    def take_damage(self, damage: int):
        self.health = max(0, self.health - max(damage - self.defense, 0))
    
    def is_alive(self) -> bool:
        return self.health > 0

    def copy(self):
        return Entity(self.name, self.health_max, self.attack, self.defense)