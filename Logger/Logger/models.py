from datetime import datetime
from enum import unique
from re import U

from sqlalchemy import (DATETIME, Column, Date, DateTime, Float, ForeignKey,
                        Integer, String, Table, Text)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

user_query = Table('search_table', Base.metadata,
                   Column('user_id', Integer, ForeignKey('user.id')),
                   Column('query_id', Integer, ForeignKey('query.id'))
                   )

query_queryresults = Table('results_table', Base.metadata,
                           Column('query_id', Integer, ForeignKey('query.id')),
                           Column('queryresult_id', Integer,
                                  ForeignKey('queryresult.id'))
                           )

saved_articles = Table('saved_articles_table', Base.metadata,
                       Column('user_id', Integer, ForeignKey('user.id')),
                       Column('queryresult_id', Integer,
                              ForeignKey('queryresult.id'))
                       )


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    pub_id = Column(String(256), unique=True)
    username = Column(
        String(60), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    saved_article = relationship(
        "QueryResult", secondary=saved_articles, backref="users",  lazy="selectin")

    def __init__(self, pub_id: str, username: str, email: str, password: str):
        self.pub_id = pub_id
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"pub_id: {self.pub_id}, user: {self.username}"

    def to_dict(self):
        dic = {
            "id": self.id,
            "pub_id": self.pub_id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        return dic


class Query(Base):
    __tablename__ = 'query'
    id = Column(Integer, primary_key=True)
    topic = Column(String(255), nullable=False, unique=True)
    seven_d_sentiment = Column(Float)
    searchers = relationship('User', secondary=user_query, backref='searches')
    query_results = relationship(
        "QueryResult", secondary=query_queryresults, backref="searched_queries",  lazy="selectin")

    def __init__(self, querys: str):
        self.topic = querys

    def to_dict(self):
        dic = {
            'id': self.id,
            'topic': self.topic,
            'weekly-sentiment': self.seven_d_sentiment
        }
        return dic


class QueryResult(Base):
    __tablename__ = 'queryresult'
    id = Column(Integer, primary_key=True)
    publisher = Column(String(255),)
    headline = Column(Text(), nullable=False)
    description = Column(Text())
    url = Column(Text())
    publish_date = Column(DateTime())
    sentiment = Column(Float)

    def __init__(self, publisher: str, headline: str, description: str, url: str, publish_date: datetime, sentiment: float):
        self.publisher = publisher
        self.headline = headline
        self.description = description
        self.url = url
        self.publish_date = publish_date
        self.sentiment = sentiment

    def to_dict(self):
        dic = {
            "publisher": self.publisher,
            "headline": self.headline,
            "description": self.description,
            "url": self.url,
            "publish_date": self.publish_date,
            "sentiment": self.sentiment
        }
        return dic
