from animal import Animal

class DomesticAnimal(Animal):
    def __init__(self, name, owner):
        super().__init__(name)
        self.owner = owner