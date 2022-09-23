import datetime

from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

user_query = database.Table('search_table',
                            database.Column(
                                'user_id', database.Integer, database.ForeignKey('user.id')),
                            database.Column('query_id', database.Integer,
                                            database.ForeignKey('query.id'))
                            )

query_queryresults = database.Table('results_table',
                                    database.Column(
                                        'query_id', database.Integer, database.ForeignKey('query.id')),
                                    database.Column('queryresult_id', database.Integer,
                                                    database.ForeignKey('queryresult.id'))
                                    )

saved_articles = database.Table('saved_articles_table',
                                database.Column(
                                    'user_id', database.Integer, database.ForeignKey('user.id')),
                                database.Column('queryresult_id', database.Integer,
                                                database.ForeignKey('queryresult.id'))
                                )


class User(database.Model):
    __tablename__ = 'user'
    id = database.Column(database.Integer, primary_key=True)
    pub_id = database.Column(database.String(256), unique=True)
    username = database.Column(
        database.String(60), unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    password = database.Column(database.String(256), nullable=False)
    saved_article = database.relationship(
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


class Query(database.Model):
    __tablename__ = 'query'
    id = database.Column(database.Integer, primary_key=True)
    topic = database.Column(database.String(255), nullable=False, unique=True)
    seven_d_sentiment = database.Column(database.Float)
    searchers = database.relationship(
        'User', secondary=user_query, backref='searches')
    query_results = database.relationship(
        "QueryResult", secondary=query_queryresults, backref="searched_querys",  lazy="selectin")

    def __init__(self, querys: str):
        self.topic = querys

    def to_dict(self):
        dic = {
            "id": self.id,
            "topic": self.topic,
            "7 day sentiment": self.seven_d_sentiment
        }
        return dic


class QueryResult(database.Model):
    __tablename__ = 'queryresult'
    id = database.Column(database.Integer, primary_key=True)
    publisher = database.Column(database.String(255))
    headline = database.Column(database.Text(), nullable=False, unique=True)
    description = database.Column(database.Text())
    url = database.Column(database.Text())
    publish_date = database.Column(database.DateTime())
    sentiment = database.Column(database.Float)

    def __init__(self, publisher: str, headline: str, description: str, url: str, publish_date: datetime, sentiment: float):
        self.publisher = publisher
        self.headline = headline
        self.description = description
        self.url = url
        self.publish_date = publish_date
        self.sentiment = sentiment

    def to_dict(self):
        dic = {
            "id": self.id,
            "publisher": self.publisher,
            "headline": self.headline,
            "description": self.description,
            "url": self.url,
            "publish_date": self.publish_date,
            "sentiment": self.sentiment
        }
        return dic
