import unittest
import Logger
from Logger import models
from sqlalchemy import create_engine, union
from sqlalchemy.orm import Session


class SimulatedTimedTriggerReq():
    """
    A class to simulate a timed request for Azure Timed Triggers.
    """

    def __init__(self):
        self.past_due = True


class TestLogger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Logger.__test_db_engine__ = create_engine(
            "sqlite+pysqlite:///:memory:", echo=True, future=True)

    def test_logger(self):
        # Set up first query for logger to use.
        models.Base.metadata.create_all(Logger.__test_db_engine__)
        session = Session(Logger.__test_db_engine__)
        query = models.Query('boris')
        session.add(query)
        session.commit()

        # Trigger Logger.
        request = SimulatedTimedTriggerReq()
        Logger.main(request)
        query_results = session.query(models.QueryResult).all()
        self.assertGreater(len(query_results), 0)

        # Trigger Logger to ensure duplicates are not added to database.
        request = SimulatedTimedTriggerReq()
        Logger.main(request)
        query_results_02 = session.query(models.QueryResult).all()
        self.assertEquals(len(query_results), len(query_results_02))

        models.Base.metadata.drop_all(Logger.__test_db_engine__)

    def test_logger_deletes_query_no_results(self):
        # Set up first query for logger to use.
        models.Base.metadata.create_all(Logger.__test_db_engine__)
        session = Session(Logger.__test_db_engine__)
        search_topic = 'asdf1234!"£$'
        query = models.Query(search_topic)
        session.add(query)
        session.commit()

        request = SimulatedTimedTriggerReq()
        Logger.main(request)
        check_for_query = session.query(
            models.Query).filter_by(topic=search_topic).first()
        self.assertEqual(check_for_query, None)

        models.Base.metadata.drop_all(Logger.__test_db_engine__)

    def test_logger_for_average_sentiment(self):
        models.Base.metadata.create_all(Logger.__test_db_engine__)
        session = Session(Logger.__test_db_engine__)
        query01 = models.Query('killed')
        query02 = models.Query('rabbit')
        session.add(query01)
        session.add(query02)
        session.commit()

        request = SimulatedTimedTriggerReq()
        Logger.main(request)
        bad = session.query(models.Query).filter_by(topic='killed').first()
        good = session.query(models.Query).filter_by(topic='rabbit').first()
        bad_sent = bad.to_dict()
        good_sent = good.to_dict()
        print(bad_sent)
        print(good_sent)
        self.assertTrue(bad_sent['weekly-sentiment'] < 0)
        self.assertTrue(good_sent['weekly-sentiment'] > 0)

        models.Base.metadata.drop_all(Logger.__test_db_engine__)


if __name__ == "__main__":
    unittest.main()
