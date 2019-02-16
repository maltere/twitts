import configparser
import twitter
import logging, sys
import sqlalchemy
import sqlalchemy.orm

APP_NAME = 'twitts'
CONFIG_FILE = 'config.ini'
TWITTER_API_SECTION = 'API'
DATABASE_API_SECTION = 'database'

# Setting Logger
LOGGER = logging.getLogger(APP_NAME)
LOGGER.setLevel(logging.DEBUG)

logging_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
logging_handler.setFormatter(formatter)
LOGGER.addHandler(logging_handler)


def get_logger():
    global LOGGER
    return LOGGER


def get_config(file=CONFIG_FILE):
    config = configparser.ConfigParser()
    get_logger().info('Read Config from %s', file)
    config.read(file)
    return config


def get_database(credentials=None):
    if not credentials:
        config = get_config()
        try:
            credentials = config[DATABASE_API_SECTION]
        except KeyError as e:
            get_logger().warning('Section %s was not found', DATABASE_API_SECTION, extra=e.__dict__)
            credentials = {}

    url = sqlalchemy.engine.url.URL(
        'postgresql',
        username=credentials.get('username'),
        password=credentials.get('password'),
        host=credentials.get('host'),
        database=credentials.get('database'),
        query={'application_name': 'rddg/twitts'}
    )

    engine = sqlalchemy.create_engine(url)
    return sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(bind=engine))


def get_api(credentials=None):
    if not credentials:
        config = get_config()
        try:
            credentials = config[TWITTER_API_SECTION]
        except KeyError as e:
            get_logger().warning('Section %s was not found', TWITTER_API_SECTION, extra=e.__dict__)
            credentials = {}

    api = twitter.Api(
        consumer_key=credentials.get('consumer_key'),
        consumer_secret=credentials.get('consumer_secret'),
        access_token_key=credentials.get('access_token_key'),
        access_token_secret=credentials.get('access_token_secret')
    )

    return api

