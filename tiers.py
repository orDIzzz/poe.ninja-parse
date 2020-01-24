import json
import re
import GUI.main


class Tiers:
    def __init__(self, contents, filter_file='HiEnd.filter', parse_file='parse.json',
                 tier_1=None, tier_2=None, tier_3=None, tierlist=None,
                 tier_1_price=12, tier_2_price=5,
                 exception=('Timeworn Reliquary Key', 'Ancient Reliquary Key', 'Tabula Rasa')):

        self.contents = contents
        self.filter_file = filter_file
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
        if tierlist is None:
            tierlist = ['1', '2', '3']
        self.tierlist = tierlist
        self.tier_1_price = abs(float(tier_1_price))
        self.tier_2_price = abs(float(tier_2_price))
        if self.tier_2_price >= self.tier_1_price:
            raise ValueError("Wrong tier prices. Tier 1 price must be more than Tier 2")
        self.exception = exception

    def take_bases(self):
        with open(self.parse_file, 'r', encoding='utf-8') as parsed:
            parsed = json.load(parsed)
            self.manage_tiers(parsed, self.contents)
        return self.tier_1, self.tier_2, self.tier_3

    def manage_tiers(self, parsed, contents):
        for n in parsed[contents]:
            item_name = n['item_name']
            price = float(n['price'])
            if self.remove_exception(item_name) is not None:
                if price > self.tier_1_price:
                    self.tier_1.append(item_name)
                elif self.tier_2_price < price <= self.tier_1_price:
                    self.tier_2.append(item_name)
                else:
                    self.tier_3.append(item_name)
        return self.tier_1, self.tier_2, self.tier_3

    def remove_exception(self, item_name):
        if item_name in self.exception:
            return None
        else:
            return item_name

    def find_lines(self):
        for tier in self.tierlist:
            with open(self.filter_file, 'r', encoding='utf-8') as filter_file:
                for index, line in enumerate(filter_file):
                    if re.search(tier, line) and re.search(self.contents.lower(), line):
                        print(f'Tier {tier} is:', line, index)
                        break

    def __repr__(self):
        return f'<Group is {self.contents}>'


class Fragments(Tiers):
    def __init__(self, contents, filter_file='HiEnd.filter', parse_file='parse.json',
                 tier_1=None, tier_2=None, tier_3=None, tierlist=None,
                 tier_1_price=12, tier_2_price=5):
        super().__init__(contents, filter_file, parse_file, tier_1, tier_2, tier_3, tier_1_price,
                         tier_2_price)
        if tierlist is None:
            self.tierlist = ['1', '2', '3', '4']

    def find_lines(self):
        for tier in self.tierlist:
            with open(self.filter_file, 'r', encoding='utf-8') as filter_file:
                for index, line in enumerate(filter_file):
                    if re.search(tier, line) \
                            and re.search(f'type->{self.contents.lower()}', line) \
                            and re.search('scarabs', line) is None:
                        print(f'Tier {tier} is:', line, index)
                        break


class Oils(Tiers):
    def __init__(self, contents, filter_file='HiEnd.filter', parse_file='parse.json',
                 tier_1=None, tier_2=None, tier_3=None, tierlist=None,
                 tier_1_price=12, tier_2_price=5):
        super().__init__(contents, filter_file, parse_file, tier_1, tier_2, tier_3, tierlist, tier_1_price,
                         tier_2_price)

    def find_lines(self):
        self.contents = 'oil'
        for tier in self.tierlist:
            with open(self.filter_file, 'r', encoding='utf-8') as filter_file:
                for index, line in enumerate(filter_file):
                    if re.search(tier, line) and re.search(f'currency->{self.contents}', line):
                        print(f'Tier {tier} is:', line, index)
                        break


class Resonators(Tiers):
    def __init__(self, contents, filter_file='HiEnd.filter', parse_file='parse.json',
                 tier_1=None, tier_2=None, tier_3=None, tierlist=None,
                 tier_1_price=12, tier_2_price=5):
        super().__init__(contents, filter_file, parse_file, tier_1, tier_2, tier_3, tierlist, tier_1_price,
                         tier_2_price)

    def find_lines(self):
        self.contents = 'resonator'
        for tier in self.tierlist:
            with open(self.filter_file, 'r', encoding='utf-8') as filter_file:
                for index, line in enumerate(filter_file):
                    if re.search(tier, line) and re.search(self.contents, line):
                        print(f'Tier {tier} is:', line, index)
                        break


class Fossils(Tiers):
    def __init__(self, contents, filter_file='HiEnd.filter', parse_file='parse.json',
                 tier_1=None, tier_2=None, tier_3=None, tierlist=None,
                 tier_1_price=12, tier_2_price=5):
        super().__init__(contents, filter_file, parse_file, tier_1, tier_2, tier_3, tier_1_price,
                         tier_2_price)
        if tierlist is None:
            self.tierlist = ['1', '2', '3', '4']

    def find_lines(self):
        self.contents = 'fossil'
        for tier in self.tierlist:
            with open(self.filter_file, 'r', encoding='utf-8') as filter_file:
                for index, line in enumerate(filter_file):
                    if re.search(tier, line) and re.search(self.contents, line):
                        print(f'Tier {tier} is:', line, index)


class Divination_cards(Tiers):
    def __init__(self, contents, filter_file='HiEnd.filter', parse_file='parse.json',
                 tier_1=None, tier_2=None, tier_3=None, tierlist=None,
                 tier_1_price=12, tier_2_price=5,
                 exception=('The Demoness', 'The Wolf\'s Shadow', "The Wolf\'s Legacy", 'The Master Artisan',
                            'A Mother\'s Parting Gift', 'Birth of the Three', 'Dark Temptation',
                            'Destined to Crumble', 'Dying Anguish', 'Lantador\'s Lost Love', 'Might is Right',
                            'Prosperity', 'Rats', 'Struck by Lightning', 'The Blazing Fire', 'The Carrion Crow',
                            'The Coming Storm', 'The Twins', 'The Hermit', 'The Incantation', 'The Inoculated',
                            'The King\'s Blade', 'The Lich', 'The Lover', 'The Surgeon', 'The Metalsmith\'s Gift',
                            'The Oath', 'The Rabid Rhoa', 'The Scarred Meadow', 'The Sigil', 'The Warden',
                            'The Watcher', 'The Web', 'The Witch', 'Thunderous Skies', 'The Deceiver',
                            'Anarchy\'s Price', 'The Wolf\'s Shadow', 'The Battle Born', 'The Feast',
                            'Assassin\'s Favour', 'Hubris', 'Rain of Chaos', 'Emperor\'s Luck', 'Her Mask',
                            'The Flora\'s Gift', 'The Puzzle', 'Boon of Justice', 'Coveted Possession',
                            'Demigod\'s Wager', 'Emperor\'s Luck', 'Harmony of Souls', 'Imperial Legacy', 'Loyalty',
                            'Lucky Connections', 'Monochrome', 'More is Never Enough', 'No Traces', 'Sambodhi\'s Vow',
                            'The Cacophony', 'The Catalyst', 'The Deal', 'The Fool', 'The Gemcutter', 'The Innocent',
                            'The Inventor', 'The Puzzle', 'The Survivalist', 'The Union', 'The Wrath',
                            'Three Faces in the Dark', 'Three Voices', 'Vinia\'s Token', 'The Seeker',
                            'Buried Treasure', 'The Journey', 'Rain of Chaos', 'Her Mask', 'The Gambler',
                            'The Flora\'s Gift', 'The Scholar')):
        super().__init__(contents, filter_file, parse_file, tier_1, tier_2, tier_3, tierlist, tier_1_price,
                         tier_2_price, exception)

    def find_lines(self):
        self.contents = 'divination'
        for tier in self.tierlist:
            with open(self.filter_file, 'r', encoding='utf-8') as filter_file:
                for index, line in enumerate(filter_file):
                    if re.search(tier, line) and re.search(self.contents, line):
                        print(f'Tier {tier} is:', line, index)
                        break


class Unique_Maps(Tiers):
    def __init__(self, contents, filter_file='HiEnd.filter', parse_file='parse.json',
                 tier_1=None, tier_2=None, tier_3=None, tierlist=None,
                 tier_1_price=12, tier_2_price=5,
                 exception=('Amber Amulet', 'Assassin Bow', 'Sapphire Ring', 'Triumphant Lamellar', 'Agate Amulet',
                            'Topaz Ring', 'Saint\'s Hauberk', 'Penetrating Arrow Quiver', 'Jade Amulet',
                            'Two-Stone Ring', 'Leather Belt', 'Imperial Skean', 'Iron Ring', 'Magistrate Crown',
                            'Murder Mitts', 'Onyx Amulet', 'Crusader Gloves', 'Studded Belt', 'Sulphur Flask',
                            'Turquoise Amulet', 'Sorcerer Boots', 'Judgement Staff', 'Stibnite Flask', 'Cobalt Jewel',
                            'Crimson Jewel', 'Viridian Jewel', 'Brass Maul', 'Clasped Boots', 'Cleaver', 'Coral Ring',
                            'Crude Bow', 'Crusader Plate', 'Crystal Wand', 'Death Bow', 'Fire Arrow Quiver', 'Gavel',
                            'Gilded Sallet', 'Gnarled Branch', 'Goathide Gloves', 'Gold Amulet', 'Golden Buckler',
                            'Great Crown', 'Great Mallet', 'Iron Circlet', 'Iron Hat', 'Iron Mask', 'Iron Staff',
                            'Ironscale Boots', 'Jade Hatchet', 'Jagged Maul', 'Latticed Ringmail', 'Leather Hood',
                            'Long Bow', 'Moonstone Ring', 'Ornate Sword', 'Painted Buckler', 'Plank Kite Shield',
                            'Plate Vest', 'Reaver Sword', 'Reinforced Greaves', 'Royal Bow', 'Royal Staff',
                            'Rusted Sword', 'Scholar Boots', 'Serrated Arrow Quiver', 'Sharktooth Arrow Quiver',
                            'Skinning Knife', 'Sledgehammer', 'Spiraled Wand', 'Strapped Leather',
                            'Tarnished Spirit Shield', 'Velvet Gloves', 'Velvet Slippers', 'Vine Circlet',
                            'War Buckler', 'Wild Leather', 'Woodsplitter')):
        super().__init__(contents, filter_file, parse_file, tier_1, tier_2, tier_3, tierlist, tier_1_price,
                         tier_2_price, exception)

    def find_lines(self):
        self.contents = 'maps'
        for tier in self.tierlist:
            with open(self.filter_file, 'r', encoding='utf-8') as filter_file:
                for index, line in enumerate(filter_file):
                    if re.search(tier, line) and re.search(f'unique->{self.contents}', line):
                        print(f'Tier {tier} is:', line, index)


class Uniques(Tiers):
    def __init__(self, contents, filter_file='HiEnd.filter', parse_file='parse.json',
                 tier_1=None, tier_2=None, tier_3=None, tierlist=None,
                 tier_1_price=12, tier_2_price=5,
                 unique_types=('Unique Jewels', 'Unique Flasks', 'Unique Weapons',
                               'Unique Armours', 'Unique Accessories')):
        super().__init__(contents, filter_file, parse_file, tier_1, tier_2, tier_3, tierlist, tier_1_price,
                         tier_2_price)
        self.unique_types = unique_types

    def take_bases(self):
        with open(self.parse_file, 'r', encoding='utf-8') as parsed:
            parsed = json.load(parsed)
            for contents in self.unique_types:
                if contents in parsed.keys():
                    self.manage_tiers(parsed, contents)
        return self.tier_1, self.tier_2, self.tier_3

    def find_lines(self):
        for tier in self.tierlist:
            with open(self.filter_file, 'r', encoding='utf-8') as filter_file:
                for index, line in enumerate(filter_file):
                    if re.search(tier, line) and re.search(f'type->{self.contents.lower()}', line):
                        print(f'Tier {tier} is:', line, index)


uniques = Uniques('Uniques')

fragments = Fragments('Fragments')
print(fragments.find_lines())

div_cards = Divination_cards('Divination Cards')

fossils = Fossils('Fossils')  # tiers are (1, 2, 4) in NeverSink's filter

resonators = Resonators('Resonators')

scarabs = Tiers('Scarabs')

oils = Oils('Oils')

incubators = Tiers('Incubators')

uni_maps = Unique_Maps('Unique Maps')  # has only 2 tiers
