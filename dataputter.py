import peewee
from models import *
import requests
from alive_progress import alive_bar


class DataPutter:
    def __init__(self):
        try:
            Items.create_table()
        except peewee.InternalError as e:
            print(str(e))
        self.active_leagues = self.__get_active_leagues()
        self.categories = self.__get_categories()
        self.__get_current_League()

    def __get_all_items(self):
        all_item = requests.get("https://api.poe.watch/itemdata").json()
        items = []
        for item in all_item:
            items.append({
                'id': item['id'],
                'name': item['name'],
                'category': item['category']
            })
        print(f'Collected {len(items)} items.')
        return items

    def __get_prices(self):
        prices = {}
        for league in self.active_leagues:
            clear_league_prices = {}
            league_prices = requests.get(f"https://api.poe.watch/compact?league={league}").json()
            for item in league_prices:
                clear_league_prices[item['id']] = item['mean']
            prices[league] = clear_league_prices
        return prices

    def get_list(self):
        prices = self.__get_prices()
        items = self.__get_all_items()[0:1100]
        with alive_bar(total=len(items), title='Scanning') as bar:
            for item in items:
                for league in self.active_leagues:
                    curr = [item_price for item_id, item_price in prices[league].items() if item_id == item['id']]
                    item[league] = curr[0] if len(curr) > 0 else 0.0
                bar()
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
        self.standard = 'Standard'
        self.standard_hc = 'Standard Hardcore'
        self.curr_league = [league['name'] for league in leagues if league['id'] == len(leagues)][0]
        self.curr_league_hc = [league['name'] for league in leagues if league['id'] == len(leagues) - 1][0]

    def save_items(self, itemlist):
        with alive_bar(title='Save items', total=len(itemlist)) as bar:
            for item in itemlist:
                try:
                    if Items.get(Items.item_id == item['id']):
                        curr_item = (Items.update(
                                standard=item['Standard'],
                                standard_hc=item['Hardcore'],
                                current=item[self.curr_league],
                                current_hc=item[self.curr_league_hc]
                                ).where(Items.item_id == item['id']))
                        curr_item.execute()
                except peewee.DoesNotExist as e:
                    curr_item = Items(
                        item_id=item['id'],
                        name=item['name'],
                        category=item['category'],
                        standard=item['Standard'],
                        standard_hc=item['Hardcore'],
                        current=item[self.curr_league],
                        current_hc=item[self.curr_league_hc]
                    )
                    curr_item.save()
                bar()

if __name__ == '__main__':
    dp = DataPutter()
    dp.save_items(dp.get_list())

