#!env/bin/python
# -*- coding: utf-8 -*- 

'''Using Webhook and self-signed certificate'''

# This file is an annotated example of a webhook based bot for
# telegram. It does not do anything useful, other than provide a quick
# template for whipping up a testbot. Basically, fill in the CONFIG
# section and run it.
# Dependencies (use pip to install them):
# - python-telegram-bot: https://github.com/leandrotoledo/python-telegram-bot
# - Flask              : http://flask.pocoo.org/
# Self-signed SSL certificate (make sure 'Common Name' matches your FQDN):
# $ openssl req -new -x509 -nodes -newkey rsa:1024 -keyout server.key -out server.crt -days 3650
# You can test SSL handshake running this script and trying to connect using wget:
# $ wget -O /dev/null https://$HOST:$PORT/

from flask import Flask, request
import telegram
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from table_def import Chat
from config import TOKEN, HOST, PORT, CERT, CERT_KEY, DB_NAME, TEXTS

engine = create_engine('sqlite:///' + DB_NAME, echo=False)
 
Session = sessionmaker(bind=engine)
session = Session()


bot = telegram.Bot(TOKEN)
app = Flask(__name__)
context = (CERT, CERT_KEY)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telegram.update.Update.de_json(request.get_json(force=True))
    m = update.message
    #text = update.message.text
    #bot.sendMessage(chat_id=update.message.chat_id, text=text)

    """
    print
    #print update.message
    m_dict = update.message.__dict__
    for key in m_dict.keys():
        print key, " : ", m_dict[key]
    print

    """
    if m:

        chat_id = m.chat.id
        cur_chat = session.query(Chat).filter(Chat.chat_id==chat_id).first()
        if cur_chat == None:
            cur_chat = Chat(chat_id)
            session.add(cur_chat)
            session.commit()

        print session.query(Chat).all()

        cur_chat = session.query(Chat).filter(Chat.chat_id==chat_id).first()

        print str(cur_chat)
        print

        if cur_chat.progress == 1:
            try:
                choice = int(m.text)
                print choice
                if not (1 <= choice and choice <= 4):
                    raise ValueError("Value must be from 1 to 4")
            except (TypeError, ValueError) as e:
                print e.message
                cur_chat.progress -= 1
            else:
                cur_chat.car_class = choice
        

        elif cur_chat.progress == 2:
            try:
                choice = int(m.text)
                print choice
                if not (100 <= choice and choice <= 999):
                    raise ValueError("Value must be from 100 to 999")
            except (TypeError, ValueError) as e:
                print e.message
                cur_chat.progress -= 1
            else:
                cur_chat.car_number = choice


        elif cur_chat.progress == 3:
            try:
                choice = int(m.text)
                print choice
                if not (1 <= choice and choice <= 2):
                    raise ValueError("Value must be from 1 to 2")
            except (TypeError, ValueError) as e:
                print e.message
                cur_chat.progress -= 1
            else:
                cur_chat.wash_type = choice
        
        elif cur_chat.progress == 4:
            if m.content_type != 'location':
                print "It is not location"
                cur_chat.progress -= 1
            else:
                print "\nLocation:"
                print type(m.location)
                print m.location
                cur_chat.location = m.location
        

        text = TEXTS[cur_chat.progress]
        if cur_chat.progress == 3:
            text += str(cur_chat)
            session.delete(cur_chat)

        print text

        #bot.sendMessage(chat_id=m.chat.id, text=text)
        bot.sendMessage(m.chat.id, text)

        cur_chat.progress += 1
        session.commit()
    
    return 'OK'



def setWebhook():
    bot.setWebhook(webhook_url='https://%s:%s/%s' % (HOST, PORT, TOKEN),
                   certificate=open(CERT, 'rb'))

if __name__ == '__main__':
    setWebhook()

    app.run(host='0.0.0.0',
            port=PORT,
            ssl_context=context,
            debug=True)
