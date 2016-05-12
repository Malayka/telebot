#!env/bin/python
from flask import Flask

app = Flask(__name__)



@app.route('/hi')
def hello():
    return 'Hi, mate'

@app.route('/bye')
def huy():
    return 'C u'


if __name__ == '__main__':

    app.run(host='0.0.0.0',
            port=5001,
            debug=True)
