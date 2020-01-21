import json


class Tiers:
    def __init__(self, groups, parse_file='parse.json',
                 tier_1=None, tier_2=None, tier_3=None,
                 tier_1_price=12, tier_2_price=5):
        self.groups = groups
        self.parse_file = parse_file
        if tier_3 is None:
            tier_3 = []
        if tier_2 is None:
            tier_2 = []
        if tier_1 is None:
            tier_1 = []
        self.tier_1 = list(tier_1)
        self.tier_2 = list(tier_2)
        self.tier_3 = list(tier_3)
        self.tier_1_price = abs(float(tier_1_price))
        self.tier_2_price = abs(float(tier_2_price))
        if self.tier_2_price > self.tier_1_price:
            raise ValueError("Wrong tier prices. Tier 1 price must be more than Tier 2")

    def take_bases(self):
        with open(self.parse_file, 'r', encoding='utf-8') as parsed:
            parsed = json.load(parsed)
            self.manage_tiers(parsed, self.groups)
        return self.tier_1, self.tier_2, self.tier_3

    def manage_tiers(self, parsed, groups):
        for n in parsed[groups]:
            item_name = n['item_name']
            price = float(n['price'])
            if price > self.tier_1_price:
                self.tier_1.append(item_name)
            elif self.tier_2_price < price <= self.tier_1_price:
                self.tier_2.append(item_name)
            else:
                self.tier_3.append(item_name)
        return self.tier_1, self.tier_2, self.tier_3

    def __repr__(self):
        return f'<Group is {self.groups}>'


class Uniques(Tiers):
    def __init__(self, groups, parse_file='parse.json',
                 tier_1=None, tier_2=None, tier_3=None,
                 tier_1_price=12, tier_2_price=5,
                 unique_types=('Unique Jewels', 'Unique Flasks', 'Unique Weapons',
                               'Unique Armours', 'Unique Accessories')):
        super().__init__(groups, parse_file, tier_1, tier_2, tier_3, tier_1_price, tier_2_price)
        self.unique_types = unique_types

    def take_bases(self):
        with open(self.parse_file, 'r', encoding='utf-8') as parsed:
            parsed = json.load(parsed)
            for groups in self.unique_types:
                if groups in parsed.keys():
                    self.manage_tiers(parsed, groups)
        return self.tier_1, self.tier_2, self.tier_3


fragments = Tiers('Fragments')
print(fragments.take_bases()[0])

oils = Tiers('Oils')

incubators = Tiers('Incubators')

scarabs = Tiers('Scarabs')

fossils = Tiers('Fossils')

resonators = Tiers('Resonators')

essences = Tiers('Essences')

div_cards = Tiers('Divination Cards')

prophecies = Tiers('Prophecies')

uni_maps = Tiers('Unique Maps')

beasts = Tiers('Beasts')

uniques = Uniques('Uniques')
print(uniques.take_bases()[0])
