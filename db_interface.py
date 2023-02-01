

from db_classes import ItemDB, PoiDB, PlaceDB, StarSystemDB, FactionDB, ResourceDB, poi_location, resource_location, \
    MarketItemDB
from session_engine import get_session

session = get_session()()


def get_poi_object(poi_id: int):
    return session.query(PoiDB).filter(PoiDB.poi_id == poi_id).first()


def get_resource_obj(resource_id: int):
    return session.query(ResourceDB).filter(ResourceDB.resource_id == resource_id).first()


def get_place_obj(place_id: int):
    return session.query(PlaceDB).filter(PlaceDB.place_id == place_id).first()


def get_item_obj(item_id: int):
    return session.query(ItemDB).filter(ItemDB.item_id == item_id).first()


def add_item(name: str, price: int):
    # TODO попытаться реализовать через декоратор блок try/except
    try:
        session.add(ItemDB(item_name=name, avg_price=price))
        session.commit()
        return 'db.Item_added'
    except Exception as ex:
        session.rollback()
        print(f'[ERROR]: {ex}')
        return



def add_star_system(sys_name: str, star_class: str):
    # TODO добавить везде блок try/except c session.rollback()
    session.add(StarSystemDB(system_name=sys_name, star_class=star_class))
    session.commit()
    print('db.system_added')


def add_place(name: str, system_id: int):
    session.add(PlaceDB(place_name=name, system_id=system_id))
    session.commit()
    print('db.place added')


def add_poi(name: str, faction_id: int):
    session.add(PoiDB(poi_name=name, faction_id=faction_id))
    session.commit()
    print('db.POI_added')


def add_resource_location(resource_id: int, place_id: int):
    resource_obj = get_resource_obj(resource_id)
    place_obj = get_place_obj(place_id)
    resource_obj.places.append(place_obj)
    session.commit()
    print('db.resource_location_added')


def add_poi_location(poi_id: int, place_id: int):
    poi_obj = get_poi_object(poi_id)
    place_obj = get_place_obj(place_id)
    poi_obj.places.append(place_obj)
    session.commit()
    print('db.poi_location_added')


def add_item_market(poi_id: int, item_id: int, buy_price: int = 0, buy_amount: int = 0, sell_price: int = 0,
                    sell_amount: int = 0):
    item = get_item_obj(item_id)
    poi = get_poi_object(poi_id)

    market = MarketItemDB(buy_price=buy_price, buy_amount=buy_amount, sell_price=sell_price, sell_amount=sell_amount)
    market.poi = poi
    market.item = item

    session.commit()
    print('db.market_item_added')


class DataCache:
    """contains data from DataBase for fast loading"""

    def __init__(self):
        self.resource_dict = self.item_dict = self.poi_dict = self.system_dict = self.place_dict = self.faction_dict = {}

        self.update_all_dicts()

    def update_resource_dict(self):
        resources = session.query(ResourceDB.resource_name, ResourceDB.resource_id).all()
        self.resource_dict = {row[0].lower(): row[1] for row in resources}

    def update_item_dict(self):
        items = session.query(ItemDB.item_name, ItemDB.item_id).all()
        self.item_dict = {row[0].lower(): row[1] for row in items}

    def update_poi_dict(self):
        pois = session.query(PoiDB.poi_name, PoiDB.poi_id).all()
        self.poi_dict = {row[0].lower(): row[1] for row in pois}

    def update_system_dict(self):
        systems = session.query(StarSystemDB.system_name, StarSystemDB.system_id).all()
        self.system_dict = {row[0].lower(): row[1] for row in systems}

    def update_place_dict(self):
        places = session.query(PlaceDB.place_name, PlaceDB.place_id).all()
        self.place_dict = {row[0].lower(): row[1] for row in places}

    def update_faction_dict(self):
        factions = session.query(FactionDB.faction_name, FactionDB.faction_id).all()
        self.faction_dict = {row[0].lower(): row[1] for row in factions}

    def update_all_dicts(self):
        self.update_system_dict()
        self.update_place_dict()
        self.update_poi_dict()
        self.update_item_dict()
        self.update_faction_dict()
        self.update_resource_dict()
        # print('refreshed', self.item_dict.keys())


class DataLoader:
    # TODO 2. Возможно отказаться вообще от этого класса
    '''
    Base Class: loads sqlalchemy objects with ORM from DB and stores
    '''
    # TODO 1. Сделать рефакторинг чтоб можно было взаимодействовать через один класс, а не кучу дочерних

    def __init__(self):
        self.session = session
        self.data = []

    def get_data(self):
        return self.data


class ResourceLoader(DataLoader):
    ''' loads sqlalchemy objects with ORM from DB and stores '''

    def load_resource(self, res_name=None):
        if res_name:
            self._load_resource_single(res_name)
        else:
            self._load_resource_current()

    def _load_resource_single(self, res_name: str, res_id: int = None):
        ''' loads single resource object to self.data'''
        # TODO: сделать так чтоб можно было передавать и name и id по желанию
        self.data = self.session.query(ResourceDB).filter(ResourceDB.resource_name == res_name).all()

    def load_resource_all(self):
        ''' loads all objects from item_table'''
        self.data = self.session.query(ResourceDB).all()

    def _load_resource_current(self):
        '''loads a tuples of indexes [(resource_id, place_id)]'''
        self.data = self.session.query(ResourceDB).join(resource_location).all()


class ItemLoader(DataLoader):
    def load_item(self, item_name=None):
        if item_name:
            self._load_item_single(item_name)
        else:
            self._load_item_current()

    def load_item_all(self):
        self.data = self.session.query(ItemDB).all()

    def _load_item_single(self, item_name: str):
        self.data = self.session.query(ItemDB).filter(ItemDB.item_name == item_name).all()

    def _load_item_current(self):
        self.data = self.session.query(ItemDB).join(MarketItemDB).all()


class TableLoader:
    '''Base Class: Takes the DataLoader instance and converts into table like: [(data, ), ]'''
    def __init__(self, obj_list: DataLoader | list = None):
        self.objects_list = []
        if isinstance(obj_list, DataLoader):
            self.objects_list = obj_list.get_data()
        elif isinstance(obj_list, list):
            self.objects_list = obj_list

        self.raw_table = []
        self.res_table = []

    def load_obj(self, obj: DataLoader):
        self.objects_list = obj.data

    def get_res_table(self):
        return self.res_table


class ResourceTable(TableLoader):
    ''' Takes the DataLoader instance and converts into table like: [(int, str,[]), ]'''
    def convert_res_data(self):
        self.raw_table = [(obj.resource_id, obj.resource_name, obj.places) for obj in self.objects_list]

    def make_resource_table(self):
        ''' :return table format [(str, str...),]'''
        self.convert_res_data()
        res_table = []
        for row in self.raw_table:
            row_table = [(row[1], el.place_name) for el in row[2]]
            res_table += row_table
        self.res_table = res_table
        return self.res_table


class ItemTable(TableLoader):
    def convert_item_data(self):
        self.raw_table = [(obj.item_id, obj.item_name, obj.pois, obj.avg_price) for obj in self.objects_list]

    def make_item_table(self):
        self.convert_item_data()
        res_table = []
        for row in self.raw_table:
            row_table = [(row[1], el.poi.poi_name, row[3], el.buy_price, el.buy_amount, el.sell_price, el.sell_amount) for el in row[2]]
            res_table += row_table
        self.res_table = res_table
        return self.res_table

    def get_headers(self):
        pass


if __name__ == '__main__':
    # dc = DataCache()
    item_load: ItemLoader = ItemLoader()
    item_load.load_item()

    item_table = ItemTable(item_load)
    item_table.convert_item_data()
    item_table.make_item_table()


    # print(item_table.raw_table)
    print(item_table.res_table)



