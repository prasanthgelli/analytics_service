import datetime as dt
import json
import pandas as pd
import numpy as np
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, func
from iotfunctions.base import BaseTransformer
from iotfunctions.metadata import EntityType
from iotfunctions.db import Database
from iotfunctions import ui
from sqlalchemy import dialects
import ibm_db

with open('credentials_as.json', encoding='utf-8') as F:
  credentials = json.loads(F.read())
db = Database(credentials = credentials)
db_schema = None

from custom.multiply_by_factor import MultiplyByFactor

db.register_functions([MultiplyByFunction])





import iotfunctions as fn
print(fn.__version__) 