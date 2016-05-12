#!env/bin/python
#-*- coding: utf-8 -*-
# table_def.py
from sqlalchemy import create_engine
from sqlalchemy import Column, SmallInteger, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from config import DB_NAME, CHAT_STR_TEXT, CHAT_SHOW_TEXT
 
engine = create_engine('sqlite:///' + DB_NAME, echo=False)
Base = declarative_base()



class Chat(Base):
    """"""
    __tablename__ = "chat"
 
    #id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, primary_key=True)                   ## primary key?????
    progress = Column(SmallInteger)

    car_class = Column(SmallInteger)
    car_number = Column(SmallInteger)
    wash_type = Column(SmallInteger)

    location = Column(String)
    wash_station = Column(String)

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.progress = 0
        self.car_class = 0
        self.car_number = 0
        self.wash_type = 0

        self.location = ""

    def __str__(self):
        return CHAT_STR_TEXT.format(self.progress, self.car_class, self.car_number, self.wash_type, self.location)

    def show(self):
        return CHAT_SHOW_TEXT.format(self.chat_id, self.progress, self.car_class, self.car_number, self.wash_type, self.location)

 
Base.metadata.create_all(engine)
