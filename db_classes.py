from sqlalchemy import Integer, Column, String, ForeignKey, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from session_engine import get_engine


engine = get_engine()
Base = declarative_base()

#_________________MANY_TO_MANY_RELATIONS_________________________________

poi_location = Table(
    "poi_location",
    Base.metadata,
    Column("poi_id", Integer, ForeignKey("poi.poi_id"), primary_key=True),
    Column("place_id", Integer, ForeignKey("place.place_id"), primary_key=True)
)

resource_location = Table(
    "resource_location",
    Base.metadata,
    Column("resource_id", Integer, ForeignKey("resource.resource_id")),
    Column("place_id", Integer, ForeignKey("place.place_id"))
)

mission_location = Table(
    "mission_location",
    Base.metadata,
    Column('mission_id', Integer, ForeignKey("mission.mission_id"), primary_key=True),
    Column('poi_id', Integer, ForeignKey("poi.poi_id"), primary_key=True),
)


class ItemDB(Base):
    __tablename__ = 'item'

    item_id = Column(Integer, primary_key=True)
    item_name = Column(String(150), unique=True)
    avg_price = Column(Integer)

    pois = relationship('MarketItemDB', back_populates='item')

    def __repr__(self):
        return f'{self.item_name} DB_obj'


class FactionDB(Base):
    __tablename__ = 'faction'

    faction_id = Column(Integer, primary_key=True)
    faction_name = Column(String(50))

    Poi = relationship("PoiDB")

    def __repr__(self):
        return f'{self.faction_name} DB_obj'


class StarSystemDB(Base):
    __tablename__ = 'star_system'

    system_id = Column(Integer, primary_key=True)
    system_name = Column(String(150))
    star_class = Column(String(20))

    Place = relationship("PlaceDB")

    def __repr__(self):
        return f'{self.system_name} DB_obj'


class ResourceDB(Base):
    __tablename__ = 'resource'

    resource_id = Column(Integer, primary_key=True)
    resource_name = Column(String(150))

    places = relationship("PlaceDB", secondary=resource_location, backref='resources')

    def __repr__(self):
        return f'{self.resource_name} DB_obj'


class PoiDB(Base):
    __tablename__ = 'poi'

    poi_id = Column(Integer, primary_key=True)
    poi_name = Column(String(150))
    faction_id = Column(Integer, ForeignKey('faction.faction_id'))

    places = relationship("PlaceDB", secondary=poi_location, backref='pois')
    items = relationship("MarketItemDB", back_populates='poi')


    def __repr__(self):
        return f'{self.poi_name} DB_obj'


class PlaceDB(Base):
    __tablename__ = 'place'

    place_id = Column(Integer, primary_key=True)
    place_name = Column(String(150))
    system_id = Column(Integer, ForeignKey('star_system.system_id'))

    def __repr__(self):
        return f'{self.place_name} DB_obj'


class MissionDB(Base):
    __tablename__ = 'mission'

    mission_id = Column(Integer, primary_key=True)
    mission_name = Column(String(200))
    trader_name = Column(String(150))

    locations = relationship('PoiDB', secondary=mission_location, backref='missions')

    def __repr__(self):
        return f'{self.mission_name} DB_obj'


#______________ASSOCIATION TABLES_____________________________
class MarketItemDB(Base):
    __tablename__ = 'market_item'

    item_id = Column(Integer, ForeignKey('item.item_id'), primary_key=True)
    poi_id = Column(Integer, ForeignKey('poi.poi_id'), primary_key=True)
    buy_price = Column(Integer)
    buy_amount = Column(Integer)
    sell_price = Column(Integer)
    sell_amount = Column(Integer)

    item = relationship("ItemDB", back_populates="pois")
    poi = relationship("PoiDB", back_populates="items")



Base.metadata.create_all(engine)



