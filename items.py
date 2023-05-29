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
            "chestplate": 5,
            "sword": 5,
            "apple": 5
        }[self.type]
        return int(baseprice * (1+0.05*(self.level%10)) * (2**int(self.level/10)))

class Coin(Item):
    def __init__(self, amount: int) -> None:
        super().__init__("coins", 1, amount)
    
    def copy(self):
        return Coin(self.amount)