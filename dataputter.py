import json
import requests
import datetime
from alive_progress import alive_bar
from pandas import DataFrame

class DataPutter:
    def __init__(self):
        self.__active_leagues = self.__get_active_leagues()
        self.categories = self.__get_categories()
        self.__get_current_League()
        self.__category_to_filter = ['enchantment', 'gem', 'base']
        self.collected_items = self.__get_list()
        self.last_update = datetime.datetime.now().strftime('%d %m %Y %H:%M:%S')
        self.df_collected_items = DataFrame(self.collected_items)

    def category_select(self, category):
        return self.df_collected_items[self.df_collected_items["category"] == category].to_dict('records')

    def __pretty_print(self, items):
        for item in items:
            print(json.dumps(item, indent=4))

    def refresh_data(self):
        self.collected_items = self.__get_list()

    def __get_all_items(self):
        items = []
        all_items = requests.get("https://api.poe.watch/itemdata").json()
        for item in all_items:
            if not item['category'] in self.__category_to_filter:
                items.append({
                    'id': item['id'],
                    'name': item['name'],
                    'category': item['category'],
                    'type': item.get('type', '')
                })
        print(f'Collected {len(items)} items.')
        return items

    def __get_prices(self):
        prices = {}
        for league in self.__active_leagues:
            clear_league_prices = {}
            league_prices = requests.get(f"https://api.poe.watch/compact?league={league}").json()
            for item in league_prices:
                clear_league_prices[item['id']] = item['mean']
            prices[league] = clear_league_prices
        return prices

    def __get_list(self):
        prices = self.__get_prices()
        items = self.__get_all_items()
        with alive_bar(total=len(items), title='Scanning') as bar:
            for item in items:
                for league in self.__active_leagues:
                    curr = [item_price for item_id, item_price in prices[league].items() if item_id == item['id']]
                    item[league] = curr[0] if len(curr) > 0 else 0.0
                bar()
        self.last_update = datetime.datetime.now()
        return items

    def __get_categories(self):
        cat_list = requests.get("https://api.poe.watch/categories").json()
        clear_cat_list = [category['name'] for category in cat_list]
        return clear_cat_list

    def __get_active_leagues(self):
        leagues = requests.get("https://api.poe.watch/leagues").json()
        active_leagues = []
        for league in leagues:
            if league['active']:
                active_leagues.append(league['name'])
        return active_leagues

    def __get_current_League(self):
        leagues = requests.get("https://api.poe.watch/leagues").json()
        self.__standard = 'Standard'
        self.__standard_hc = 'Standard Hardcore'
        self.__curr_league = [league['name'] for league in leagues if league['id'] == len(leagues)][0]
        self.__curr_league_hc = [league['name'] for league in leagues if league['id'] == len(leagues) - 1][0]
