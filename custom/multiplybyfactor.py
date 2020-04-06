import inspect
import logging
import datetime as dt
import math
from sqlalchemy.sql.sqltypes import TIMESTAMP,VARCHAR
import numpy as np
import pandas as pd

from iotfunctions.base import BaseTransformer,BaseComplexAggregator
from iotfunctions import ui


PACKAGE_URL = 'git+https://github.com/prasanthgelli/analytics_service@master'

class Sdd(BaseComplexAggregator):
    _abort_on_fail = True
    _allow_empty_df = False
    # _discard_prior_on_merge = True
    requires_input_items = True
    produces_output_items = True
    def __init__(self, area_column, distance_column, name):
        super().__init__()
        self.area_column = area_column
        self.distance_column = distance_column
        self._input_set = set([self.area_column, self.distance_column])
        self.output_item = name
        self._output_list = [self.output_item]
    def get_input_set(self):
        return self._input_set
    def execute(self, df=None, start_ts=None, end_ts=None, entities=None):
        logger.debug('df_input=%s' % log_df_info(df, head=5))
        grouper = self.granularity.grouper
        logger.debug('grouper=%s' % str(grouper))
        df['_total_area'] = df[self.area_column].sum()
        df['_weight'] = df[self.area_column] / df['_total_area']
        df['_weighted_distance'] = df['_weight'] * df[self.distance_column]
        df = df.drop(columns=['_total_area'])
        df = df.groupby(grouper).agg({'_weight':'sum', '_weighted_distance':'sum'})
        df = df.reset_index()
        logger.debug('df=%s' % log_df_info(df, head=5))
        df = df['_weighted_distance'] / df['_weight']
        logger.debug('final_df=%s' % log_df_info(df, head=5))
        return df
    @classmethod
    def build_ui(cls):
        inputs = []
        inputs.append(UISingleItem(name='area_column', datatype=float, required=True, description='The area column.'))
        inputs.append(UISingleItem(name='distance_column', datatype=float, required=True, description='The distance column.'))
        outputs = []
        outputs.append(UIFunctionOutSingle(name='name', datatype=float, description='The distance between source and target points.'))
        return (inputs, outputs)

# class meangp(BaseTransformer):

#     def __init__(self, input_items,output_items):
#         print("Here")
#         self.input_items = input_items
#         self.output_items = output_items
#         super().__init__()
#     def execute(self, df):
#         df = df.copy()
#         for i,input_item in enumerate(self.input_items):
#             df[self.output_items[i]] = df[input_item] * 3
#         return df
#     @classmethod
#     def build_ui(cls):
#         #define arguments that behave as function inputs
#         inputs = []
#         inputs.append(ui.UIMultiItem(
#                 name = 'input_items',
#                 datatype=float,
#                 description = "Data items adjust",
#                 output_item = 'output_items',
#                 is_output_datatype_derived = True)
#                       )        
#         outputs = []
#         return (inputs,outputs)
