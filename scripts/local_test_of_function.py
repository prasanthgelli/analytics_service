import datetime as dt
import json
import pandas as pd
import numpy as np
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, func
from iotfunctions.base import BaseTransformer
from iotfunctions.metadata import EntityType
from iotfunctions.db import Database
from iotfunctions import ui

with open('credentials_as.json', encoding='utf-8') as F:
  credentials = json.loads(F.read())
db_schema = None
db = Database(credentials=credentials)

from custom.multiplybyfactor import MultiplyByFactor
fn = MultiplyByFactor(
    input_items = ['orgoccupancycount', 'occupancycount'],
    factor = 2,
    output_items = ['adjusted_orgoccupancycount', 'adjusted_occupancycount']
              )
df = fn.execute_local_test(db=db, db_schema=db_schema, generate_days=1,to_csv=True)
print(df)