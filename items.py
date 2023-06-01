class Item:
    def __init__(self, type: str, level: int, amount: int) -> None:
        self.type = type
        self.level = level
        self.amount = amount

    def from_tuple(tuple):
        return Item(tuple[0], tuple[1], tuple[2])

    def to_tuple(self) -> tuple[str, int, int]:
        return (self.type, self.level, self.amount)

    def copy(self):
        return Item(self.type, self.level, self.amount)
    
    def determine_price(self) -> int:
        baseprice = {
            "chestplate": 20,
            "sword": 20,
            "apple": 20
        }[self.type]
        return int(baseprice * (1+0.05*(self.level%10)) * (2**int(self.level/10)))

    def __eq__(self, __value: object) -> bool:
        return self.type == __value.type and self.level == __value.level and self.amount == __value.amount
    
    def __hash__(self) -> int:
        return hash((self.type, self.level, self.amount))
    
    def __str__(self) -> str:
        return f"{self.type.capitalize()}{f' T{self.level}' if self.level > 0 else ''}"

class Coin(Item):
    def __init__(self, amount: int) -> None:
        super().__init__("coins", 1, amount)
    
    def copy(self):
        return Coin(self.amount)