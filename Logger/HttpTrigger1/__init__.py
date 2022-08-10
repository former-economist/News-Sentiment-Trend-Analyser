import pytz
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
from .scraper_funcs import create_search_string, create_instance, create_dated_instance, search, analysis_sentiment

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

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    global __test_db_connection_string__

    if req.method == "POST":
        try: 
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse("No Json body was sent.", status_code=304)

    search_string = ""

    try:
        search_string = req_body["search-string"]
    except ValueError:
        return func.HttpResponse("No Json body sent", status_code=400)

    search_instance = create_instance()
    found_articles = search(search_string, search_instance)
    if len(found_articles) > 0:
        analysis_sentiment(found_articles)

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

    query = session.query(models.Query).filter_by(topic=search_string).first()

    for article in found_articles:
        article_publisher = article['publisher']['title']
        article_headline = article['title']
        article_desc = article['description']
        article_url = article['url']
        article_date = dateparser.parse(article['published date'])
        article_sentiment = article['sentiment']

        does_exist = session.query(models.QueryResult).filter_by(headline=article_headline).first()
        # is_there = session.query(does_exist.exists()).scalar()

        if not does_exist:

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
            # Add to query to query_queryresult association table
            result.searched_queries.append(query)
            
        else:
            query_result = does_exist
            query_result.searched_queries.append(query)
    session.commit()
    utc = pytz.utc

    date_limit = datetime.today() - timedelta(days=7)
    new_date_limit = utc.localize(date_limit)

    total = 0.0
    count = 0.0
    for result in query.query_results:
        result_date = result.publish_date.replace(tzinfo=utc)
        if result_date > new_date_limit:
            total += result.sentiment
            count += 1.0
    
    if count > 0.0:
            avg = total / count
    
            query.seven_d_sentiment = avg
            session.commit()
            session.close()
            logging.info(avg)
            return func.HttpResponse("Recieved", status_code=200)

