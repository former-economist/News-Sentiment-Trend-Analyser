from genericpath import exists
from sqlite3 import IntegrityError
import azure.functions as func
import datetime
from datetime import datetime, timedelta
import logging
from . import models
import os
import dateparser
import sqlalchemy
from sqlalchemy import exc, delete
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from .scraper_funcs import create_search_string, create_instance, create_dated_instance, search, analysis_sentiment, calculate_sentiment

__test_db_engine__ = None


def database_uri() -> str:
    """
    Function to build the database connection string, using settings taken
    from environment variables.

    Returns:
        str: Database connection String.
    """

    # If the connection string has been given, use it.
    url = os.environ.get("DB_CONNECTION_STRING", default="")
    if len(url) != 0:
        return url

    url = sqlalchemy.engine.url.URL.create(
        drivername="mariadb+mariadbconnector",
        username=os.environ.get("DB_USER", default="none"),
        password=os.environ.get("DB_PASSWORD", default="none"),
        host=os.environ.get("DB_SERVER", default="127.0.0.1"),
        port=os.environ.get("DB_PORT", default="3306"),
        database=os.environ.get("DB_NAME", default="mydb"))
    return str(url)


def main(mytimer: func.TimerRequest) -> None:
    """
    Timer function to collect QueryResult object for
    all Query objects in database.

    Args:
        mytimer (func.TimerRequest): timer request base on CRON expression.
    """
    global __test_db_connection_string__

    #Get or create and engine
    if __test_db_engine__ is not None:
        engine = __test_db_engine__
    else:
        # Get the connection variable andd SSl certificate if it has been provided.
        connection_string = database_uri()
        ssl_cert = os.environ.get("DB_SSL_CERT", default=None)
        connection_args = {}
        if ssl_cert is not None:
            connection_args["ssl_ca"] = ssl_cert
        engine = sqlalchemy.create_engine(
            connection_string, connect_args=connection_args, echo=True, future=True)

    models.Base.metadata.create_all(engine)
    session = Session(engine)

    statement = sqlalchemy.select(models.Query)
    queries = session.execute(statement)

    dic = {}
    for query in queries.scalars():
        todays_news = create_instance()
        search_topic = str(query.topic)
        found_articles = search(search_topic, todays_news)
        if len(found_articles) == 0:
            session.delete(query)
            session.commit()
        else:
            # analysis_sentiment(found_articles)
            for article in found_articles:
                article_publisher = article['publisher']['title']
                article_headline = article['title']
                article_desc = article['description']
                article_url = article['url']
                article_date = dateparser.parse(article['published date'])
                article_sentiment = calculate_sentiment(article=article)
                # article_sentiment = article['sentiment']

                does_exist = session.query(models.QueryResult).filter(
                    models.QueryResult.headline == article_headline)
                is_there = session.query(does_exist.exists()).scalar()

                if not is_there:

                    # Create new QueryResult
                    result = models.QueryResult(
                        article_publisher,
                        article_headline,
                        article_desc,
                        article_url,
                        article_date,
                        article_sentiment
                    )

                    

                    # Add to database
                    session.add(result)
                    result.searched_queries.append(query)
                    
                else:
                    query_result = does_exist.first()
                    query_result.searched_queries.append(query)
        session.commit()

        date_limit = datetime.today() - timedelta(days=7)

        query_table = session.query(models.Query)

        #This is ridiculously slow, fix it.

        # Find average sentiment for last seven days and update query sentiment.
        for query in query_table:
            total = 0.0
            count = 0.0
            for result in query.query_results:
                if result.publish_date > date_limit:
                    total += result.sentiment
                    count += 1.0

        
            if count > 0.0:
                avg = total / count

                query.seven_d_sentiment = avg
                session.commit()
                logging.info(avg)
    session.close()
