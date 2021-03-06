# Opportunity to generate a DAO for Sqlite3 in Python 3

# Author: Soft9000.com
# 2018/03/08: Class Created
# Status: Code Complete. Alpha.

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.SchemaDef.Order import OrderDef
from SqltDAO.CodeGen01.DaoExceptions import *
from SqltDAO.CodeGen01.SqlDetect import SqlDetect
from SqltDAO.CodeGen01.SqlSyntax import SqliteCrud


class DaoGen:

    def __init__(self):
        pass

    def get_fields(self, order, data_file, sep=','):
        '''
        Populate an OrderDef using a OrderClass + data_file.
        Returns OrderDef + Fields detected upon success,
        or an Exception on error.
        '''
        if isinstance(order, OrderClass) is False:
            raise TypeError("Instance of OrderClass is required.")
        if os.path.exists(data_file) is False:
            raise IOError("Data file not found.")
        header = SqlDetect.GetHeader(data_file, sep=sep)
        if header is None:
            raise IOError("Header not found.")
        fields = SqlDetect.GetFields(data_file, sep=sep)
        result = OrderDef.Create(order, fields)
        return fields, result

    def gen_code(self, order, data_file, sep=','):
        ''' Detect tables & save THE CODE for a given a data_file.
        True or Exception returned.
        '''
        fields, order2 = self.get_fields(order, data_file, sep)
        if fields is None:
           raise GenException("Error: SqlDetect.GetFields has None.")
        sql = SqliteCrud(order, fields)
        return sql.code_class_template(data_file, sep=sep)

    def gen_order(self, order, data_file, sep=','):
        ''' Detect tables & write THE ORDER FILE for a given data_file.
        True or Exception returned.
        '''
        fields, order2 = self.get_fields(order, data_file, sep)
        if fields is None:
           raise GenException("Error: SqlDetect.GetFields has None.")
        return OrderDef.SaveFile(order2, overwrite=True)

    def write_code(self, order, data_file, sep=','):
        ''' Write CODE from an OrderClass using data from an arbitrary input / data_file.
        True or Exception returned.
        '''
        source = self.gen_code(order, data_file, sep=sep)
        with open(order.file_name, "w") as fh:
            fh.write(source)
            return True
        return False

