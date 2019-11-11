from functions import get_lands, get_lord

class Land:
    def __init__(self, name, owner, buildings, religion):
        self.name = name
        self.buildings = buildings
        self.owner_id = owner
        self.income = 300
        self.religion = religion

    def build(self, name_of_building, lords):
        if len(self.buildings) < 2:
            if name_of_building.lower() == 'расширение поселения' or name_of_building.lower() == 'поселение' and get_lord(self.owner_id, lords).money >= 1200:
                self.buildings.append('расширение поселения')
                get_lord(self.owner_id, lords).money -= 1200
                return True
            elif name_of_building.lower() == 'мастерская оружейника' and get_lord(self.owner_id, lords).money >= 600:
                self.buildings.append('мастерская оружейника')
                get_lord(self.owner_id, lords).money -= 600
                return True
            elif name_of_building.lower() == 'мастерская лучника' and get_lord(self.owner_id, lords).money >= 600:
                self.buildings.append('мастерская лучника')
                get_lord(self.owner_id, lords).money -= 600
                return True
            elif name_of_building.lower() == 'коннозаводчик' and get_lord(self.owner_id, lords).money >= 600:
                self.buildings.append('коннозаводчик')
                get_lord(self.owner_id, lords).money -= 600
                return True
            elif name_of_building.lower() == 'крепость' and get_lord(self.owner_id, lords).money >= 2000:
                self.buildings.append('крепость')
                get_lord(self.owner_id, lords).money -= 2000
                return True
            else:
                return False


class Lord:
    def __init__(self, id, money, king, church_lord, religion):
        self.id = id
        self.money = money
        self.king_id = king
        self.church_lord_id = church_lord
        self.religion = religion

    def income(self, lands, lords):
        income = 0
        lands1 = get_lands(self, lands)
        for land in lands1:
            if 'расширение поселения' in land.buildings:
                if self.religion == land.religion:
                    income += 600
                else:
                    income += 300
            else:
                if self.religion == land.religion:
                    income += 300
                else:
                    income += 150
        get_lord(self.church_lord_id, lords).money += income // 10
        income -= income // 10
        if self.king_id is not None:
            king = get_lord(self.king_id, lords)
            king.money += king.tax * income // 100
            income -= king.tax * income // 100
        self.money += income

    def pay(self, to, n, lords):
        if self.money >= n > 0:
            self.money -= n
            get_lord(to, lords).money += n
            return True
        return False

    def __str__(self):
        return f"owner id: {self.id}; money: {self.money}; king id: {self.king_id}; church lord id: {self.church_lord}; religion: {self.religion}"

    def list(self):
        return [self.id, self.money, self.king_id, self.church_lord_id, self.religion, None]

class King(Lord):
    def __init__(self, id, money, church_lord, religion, tax):
        super().__init__(id, money, None, church_lord, religion)
        self.tax = tax

    def list(self):
        return [self.id, self.money, None, self.church_lord_id, self.religion, self.tax]

class Church_lord(Lord):
    def __init__(self, id, money, king_name, church_lord, religion):
        super().__init__(id, money, king_name, church_lord, religion)

    def income(self, lands, lords):
        pass
