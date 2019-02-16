# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, Boolean, text as text_a
from sqlalchemy.types import Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'twitter'}

    user_id = Column(BigInteger, primary_key=True)
    screen_name = Column(String(20), nullable=False)
    created_at = Column(String, nullable=False)


class Tweet(Base):
    __tablename__ = 'tweet'
    __table_args__ = {'schema': 'twitter'}

    tweet_id = Column(BigInteger, primary_key=True)
    json = Column(JSONB(astext_type=Text()))
    text = Column(String(250), nullable=False)
    created_at = Column(DateTime(True), nullable=False)
    hashtags = Column(JSONB(astext_type=Text()))
    retweet_id = Column(ForeignKey('twitter.tweet.tweet_id', ondelete='RESTRICT', onupdate='CASCADE'))
    source = Column(String(400))
    created_from_id = Column(ForeignKey('twitter.user.user_id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    delete_next = Column(Boolean, nullable=False, server_default=text_a("false"))
    deleted = Column(Boolean, nullable=False, server_default=text_a("false"))


    created_from = relationship('User')
    retweet = relationship('Tweet', remote_side=[tweet_id])
