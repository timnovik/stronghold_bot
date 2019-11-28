from functions import get_lands, get_lord, get_feods, get_feod


def get_data(a, b, c):
    global lands, lords, feods
    lands = a
    lords = b
    feods = c


class Land:
    def __init__(self, name, feod, buildings, religion):
        self.name = name
        self.buildings = buildings
        self.feod_name = feod
        self.religion = religion

    def income(self):
        return 300 if 'расширение поселения' not in self.buildings else 600

    def build(self, name_of_building):
        self.owner_id = get_feod(self.feod_name)
        if len(self.buildings) < 2:
            if name_of_building.lower() == 'расширение поселения' or name_of_building.lower() == 'поселение' and get_lord(self.owner_id, lords).money >= 1200:
                self.buildings.append('расширение поселения')
                get_lord(self.owner_id).money -= 1200
                return True
            elif name_of_building.lower() == 'мастерская оружейника' and get_lord(self.owner_id).money >= 600:
                self.buildings.append('мастерская оружейника')
                get_lord(self.owner_id).money -= 600
                return True
            elif name_of_building.lower() == 'мастерская лучника' and get_lord(self.owner_id).money >= 600:
                self.buildings.append('мастерская лучника')
                get_lord(self.owner_id).money -= 600
                return True
            elif name_of_building.lower() == 'коннозаводчик' and get_lord(self.owner_id).money >= 600:
                self.buildings.append('коннозаводчик')
                get_lord(self.owner_id).money -= 600
                return True
            elif name_of_building.lower() == 'крепость' and get_lord(self.owner_id).money >= 2000:
                self.buildings.append('крепость')
                get_lord(self.owner_id).money -= 2000
                return True
            else:
                return False


class Feod:
    def __init__(self, name, owner, war):
        self.name = name
        self.owner_id = owner
        self.war = war

    def income(self, religion):
        res = 0
        if not self.war:
            a = 0
        for land in get_lands(self):
            res += land.income() if religion == land.religion else land.income() // 2
        return res


class Lord:
    def __init__(self, id, money, king, church_lord, religion):
        self.id = id
        self.money = money
        self.king_id = king
        self.church_lord_id = church_lord
        self.religion = religion

    def income(self):
        income = 0
        for feod in get_feods(self):
            income += feod.income(self.religion)
        get_lord(self.church_lord_id).money += income // 10
        income -= income // 10
        if self.king_id is not None:
            king = get_lord(self.king_id)
            king.money += king.tax * income // 100
            income -= king.tax * income // 100
        self.money += income

    def pay(self, to, n):
        if self.money >= n > 0:
            self.money -= n
            get_lord(to).money += n
            return True
        return False

    def __str__(self):
        return f"owner id: {self.id}\nmoney: {self.money}\nking id: {self.king_id}\nchurch lord id: {self.church_lord_id}\nreligion: {self.religion}"

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

    def income(self):
        pass
