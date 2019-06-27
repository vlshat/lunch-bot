from os import environ
from flask import Flask
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('starting web app')


app = Flask(__name__)


@app.route('/')
def index():
    logger.info('up and running')
    return 'Ok'


app.run(host= '0.0.0.0', port=environ.get('PORT'))
