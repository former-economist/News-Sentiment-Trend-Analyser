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
        Logger.__test_db_engine__ = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
    
    def test_logger(self):
        # Set up first query for logger to use.
        models.Base.metadata.create_all(Logger.__test_db_engine__)
        session = Session(Logger.__test_db_engine__)
        query = models.Query('boris')
        session.add(query)
        session.commit()

        #Trigger Logger.
        request = SimulatedTimedTriggerReq()
        Logger.main(request)
        query_results = session.query(models.QueryResult).all()
        self.assertEqual(len(query_results), 99)

        #Trigger Logger again to ensure duplicates are not added
        request = SimulatedTimedTriggerReq()
        Logger.main(request)
        query_results = session.query(models.QueryResult).all()
        self.assertEqual(len(query_results), 99)

if __name__ == "__main__":
    unittest.main()