import twitts
from twitts.db import Tweet, User
from dateutil import parser

orm = twitts.get_database()
api = twitts.get_api()
logger = twitts.get_logger()

api.VerifyCredentials()

start = 9999999999999999999999
max_id = start
count = 1
found = 0


def get_user(json):
    global orm, logger
    user_id = json.get('id')

    user = orm.query(User).filter(User.user_id == user_id).one_or_none()

    if not user:
        logger.info('User not found, inserting based on json data')
        created_at = parser.parse(json.get('created_at'))
        user = User(
            user_id=json.get('id'),
            screen_name=json.get('screen_name'),
            created_at=created_at
        )
        session = orm()
        session.add(user)
        session.commit()

    return user


def get_tweet(tweet_id):
    tweet = orm.query(Tweet).filter(Tweet.tweet_id == tweet_id).one_or_none()
    return tweet


def insert_tweet(json):
    global orm, logger

    tweet_id = json.get('id')

    user = get_user(json.get('user'))
    retweet = None

    tweet = get_tweet(tweet_id)

    if not tweet:
        if json.get('retweeted_status'):
            retweet = insert_tweet(json.get('retweeted_status'))

        logger.info('Inserting Tweet %s', tweet_id)

        created_at = parser.parse(json.get('created_at'))
        tweet = Tweet(
            tweet_id=tweet_id,
            json=json,
            text=json.get('text'),
            created_at=created_at,
            hashtags=json.get('hashtags'),
            retweet=retweet,
            source=json.get('source'),
            created_from=user
        )
        session = orm()
        session.add(tweet)
        session.add(user)
        session.commit()

    return tweet


logger.info('Starting calling API')

while count > 0:
    if max_id == start:
        query = api.GetUserTimeline(count=150)
    else:
        query = api.GetUserTimeline(max_id=max_id, count=150)
    count = len(query)
    max_new_id = max_id
    for s in query:
        found += 1
        max_new_id = s.id
        insert_tweet(s._json)

    logger.info('Query max: %s done, Length %s', max_id, count)
    max_id = max_new_id-1
