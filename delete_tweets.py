import twitts
import twitter
from twitts.db import Tweet, User
from dateutil import parser

USERNAME = ''
UNTIL = '2000-12-31 00:00:00 +0000'

orm = twitts.get_database()
api = twitts.get_api()
logger = twitts.get_logger()

api.VerifyCredentials()

user = orm.query(User).filter(User.screen_name == USERNAME).one_or_none()
tweets = orm.query(Tweet)\
    .filter(Tweet.created_from == user)\
    .filter(Tweet.delete_next.is_(True))\
    .filter(Tweet.deleted.isnot(True))\
    .filter(Tweet.created_at < parser.parse(UNTIL))\
    .order_by(Tweet.tweet_id.asc())\
    .all()

for tweet in tweets:
    if not tweet.deleted:
        try:
            logger.info('Delete Tweet %s from %s', tweet.tweet_id, tweet.created_at)
            api.DestroyStatus(tweet.tweet_id)
        except twitter.TwitterError as e:
            for message in e.message:
                if message.get('code') == 144:
                    logger.info('Tweet already deleted: %s', tweet.tweet_id, extra={'err_message': message})
                else:
                    logger.error('Exception raised with unknown code', extra={'err_message': message})
        finally:
            session = orm()
            tweet.deleted = True
            session.add(tweet)
            session.commit()
