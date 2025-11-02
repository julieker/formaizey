#!/usr/bin/env python3
""" save conversation history
"""

########### The purpose of this module is to save conversation history and retriece it when the button is clicked in vue.js

############### sqlalchemy is a library in python that lets you refer to the database structure in terms of objects ...
############### much like Hibernate does for Java.  You map the tables and columns to objects. 

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

#########retrieve the database conection string from the environment variable DATABASE_URL_JULIE.   This is set in ny .zprofile.
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
######################## Create a class called MaizeyHistory that is mapped to table maizey_history.   Map the columns into objects as well.
class MaizeyHistory(Base):
    __tablename__ = 'maizey_history'
    id = Column(Integer, primary_key=True)
    user_message = Column(String, nullable=False)
    maizey_response = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# ---- Insert function ---- 
################  The insert_history function sets a record to an instance of the MaizeyHistory object 
###############   with the given message and response.   When the record is added this inserts a record into the database.
##############    This is called in the flask server when ever there is a message and response. 
def insert_history(user_msg, maizey_resp):
    record = MaizeyHistory(
        user_message=user_msg,
        maizey_response=maizey_resp,
        timestamp=datetime.utcnow()
    )
    session.add(record)
    session.commit()
    print(f"Inserted record with id: {record.id}")


###########################################
################ This routine retrieves records from the maizey_history table using the  MaizeyHistory object.
###############  A session is started and rows are retrieved into the array result and returned. 
##############   This is used in the MaizeyVue "Show History" button to see the history.
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

