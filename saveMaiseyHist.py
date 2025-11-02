#!/usr/bin/env python3
""" save conversation history
"""

from sqlalchemy import tuple_, or_, update, not_, and_
from sqlalchemy import select
from sqlalchemy.orm import aliased, joinedload

import os
import sys
import argparse
import csv
import hashlib
from datetime import datetime
import logging
from typing import Dict, List, Set, Tuple
import pandas as pd
from sqlalchemy import create_engine, text, Table, Column, Integer, String, Boolean, ForeignKey, MetaData, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from contextlib import contextmanager
from dateutil.parser import parse

shortcodeLabMapping = {}



# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
db_url = os.environ.get('DATABASE_URL_JULIE')
print ("here is db url:") 
print (db_url) 
if not db_url:
    raise ValueError("DATABASE_URL environment variable is required")
engine = create_engine(db_url)
# Global variables
Base = declarative_base()


Session = sessionmaker(bind=engine)
session = Session()




metadata = MetaData()
#shortcodes_to_update = [] 



# ---- Table mapping ----
class MaizeyHistory(Base):
    __tablename__ = 'maizey_history'
    id = Column(Integer, primary_key=True)
    user_message = Column(String, nullable=False)
    maizey_response = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# ---- Insert function ----
def insert_history(user_msg, maizey_resp):
    record = MaizeyHistory(
        user_message=user_msg,
        maizey_response=maizey_resp,
        timestamp=datetime.utcnow()
    )
    session.add(record)
    session.commit()
    print(f"Inserted record with id: {record.id}")



def get_history():
    session = Session()  # your SQLAlchemy session function
    rows = session.query(MaizeyHistory).order_by(MaizeyHistory.timestamp.asc()).all()
    result = []
    for row in rows:
        result.append({
            "user_message": row.user_message,
            "maizey_response": row.maizey_response,
            "timestamp": row.timestamp.isoformat()
        })
    session.close()
    return result







Base.metadata.create_all(engine)
    
# Insert a history row
insert_history("Hello, Maizey!", "Hi there, human!")
the_result = get_history()

print (the_result);


print ("hi")

