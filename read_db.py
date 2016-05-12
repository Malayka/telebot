#!env/bin/python
# -*- coding: utf-8 -*-
from config import TOKEN, DB_NAME
import telebot

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def import Chat

engine = create_engine('sqlite:///' + DB_NAME, echo=False)
 
Session = sessionmaker(bind=engine)
session = Session()

chats = session.query(Chat).all()
for chat in chats:
    print chat.show()