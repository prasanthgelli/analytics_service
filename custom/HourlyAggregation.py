# *****************************************************************************
# Â© Copyright IBM Corp. 2018.  All Rights Reserved.
#
# This program and the accompanying materials
# are made available under the terms of the Apache V2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
# *****************************************************************************

import datetime as dt
import logging
import warnings
import numpy as np
import pandas as pd
from sqlalchemy import (Table, Column, Integer, SmallInteger, String, DateTime)

from pandas.api.types import (is_string_dtype, is_numeric_dtype, is_bool_dtype,
                              is_datetime64_any_dtype, is_dict_like)

from iotfunctions.db import SystemLogTable
from iotfunctions.metadata import EntityType
from iotfunctions.automation import TimeSeriesGenerator
from iotfunctions.base import (BaseTransformer, BaseDataSource, BaseEvent,BaseFilter,
                               BaseAggregator, BaseDatabaseLookup, BaseDBActivityMerge,
                               BaseSCDLookup, BaseMetadataProvider, BasePreload)
from iotfunctions import ui

'''
This module contains a number of sample functions. 
'''

logger = logging.getLogger(__name__)

PACKAGE_URL = 'git+https://github.com/prasanthgelli/analytics_service@@starter_package'
    
    
class PIRHourlyAgg(BaseAggregator):
    '''
    Demonstration a hourly aggregation
    '''
    def __init__(self, input_item, output_item):
        self.input_item = input_item
        self.output_item = output_item
        super().__init__()

    def _calc(self, df):
        sql="select MOTION from IOT_PIR_MOTION where RCV_TIMESTAMP_UTC > '2019-09-11 05:00:00.000'"
        bdl = BaseDatabaseLookup(
             lookup_table_name = 'IOT_PIR_MOTION',
             lookup_keys= ['MOTION'],
             lookup_items = ['MOTION'],
             sql=sql		 
             )
        pdf = bdl.execute(df=None)
        df[self.output_item] = df[self.input_item].min()
        return df
		
    @classmethod
    def build_ui(cls):

        # define arguments that behave as function inputs
        inputs = []
        inputs.append(ui.UISingleItem(
            name='input_item',
            datatype=float,
            description='Choose an item to aggregate',
            required=True,
            ))
        outputs = [
            ui.UIFunctionOutSingle(name='output_item', datatype=float)
        ]
        return (inputs,outputs)
