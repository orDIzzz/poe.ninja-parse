import json
import pickle

tier1 = 12
tier2 = 5


def tiers(parse_file, value_tier_1=12, value_tier_2=5):
    tier = {'tier_1': [], 'tier_2': [], 'tier_3': []}
    with open(parse_file, 'r', encoding='utf-8') as parse_file:
        parsed = json.load(parse_file)
        all_items = dict()
        for p in parsed.keys():
            for n in parsed[p]:
                item_name = n['item_name']
                price = float(n['price'])
                if price > value_tier_1:
                    tier['tier_1'].append(item_name)
                elif value_tier_2 < price <= value_tier_1:
                    tier['tier_2'].append(item_name)
                else:
                    tier['tier_3'].append(item_name)
            all_items[p] = tier
            tier = {'tier_1': [], 'tier_2': [], 'tier_3': []}
        manage_categories(all_items)
        print(all_items.keys())
    return all_items


def manage_categories(all_items):
    unique_dict = {'Uniques': {'tier_1': [], 'tier_2': [], 'tier_3': []}}
    uniques = 'Unique Jewels', 'Unique Flasks', 'Unique Weapons', 'Unique Armours', 'Unique Accessories'
    for types in all_items.keys():
        if types in uniques:
            for p in all_items[types].pop('tier_1'):
                unique_dict['Uniques']['tier_1'].append(p)
            for p in all_items[types].pop('tier_2'):
                unique_dict['Uniques']['tier_2'].append(p)
            for p in all_items[types].pop('tier_3'):
                unique_dict['Uniques']['tier_3'].append(p)
    all_items.update(unique_dict)
    all_items_copy = all_items.copy()
    for k in all_items_copy.keys():
        for i in uniques:
            if i == k:
                all_items.pop(i)
    return all_items


def save_tiers(parser):
    with open('tiers.csv', 'w', encoding='utf-8') as sorted_items:
        sorted_items.write(str(tiers(parser, tier1, tier2)))

    with open('tiers.pickle', 'wb') as sorted_items2:
        pickle.dump(tiers(parser, tier1, tier2), sorted_items2)


save_tiers('parse.json')

# unique = 'Unique Jewels', 'Unique Flasks', 'Unique Weapons', 'Unique Armours', 'Unique Accessories'
