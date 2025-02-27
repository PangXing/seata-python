# -*- coding: utf-8 -*-

"""
 Licensed to the Apache Software Foundation (ASF) under one or more
 contributor license agreements.  See the NOTICE file distributed with
 this work for additional information regarding copyright ownership.
 The ASF licenses this file to You under the Apache License, Version 2.0
 (the "License"); you may not use this file except in compliance with
 the License.  You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

from am.mysql_base import InsertStatement

from seata.sqlparser.SQLParsingException import SQLParsingException
from seata.sqlparser.mysql.MySQLDmlRecognizer import MySQLInsertRecognizer
from seata.sqlparser.mysql.antlr4.value import MySQLValue
from seata.sqlparser.mysql.antlr4.value.MySQLValue import NotPlaceholderValue
from seata.sqlparser.mysql.antlr4.visit.MySQLInsertStatement import MySQLInsertStatement


class MySQLInsertRecognizer(MySQLInsertRecognizer):

    def __int__(self, original_sql=None, sql_type=None, stmt=None):
        self.original_sql = original_sql
        self.sql_type = sql_type
        self.stmt = stmt
        self.statement = None

    def init(self):
        if not isinstance(self.stmt, InsertStatement):
            raise TypeError('stmt type error.' + type(self.stmt).__name__)
        self.statement = MySQLInsertStatement(self.stmt)

    def get_sql_type(self):
        return self.sql_type

    def get_table_name(self):
        return self.statement.table_name

    def get_table_alias(self):
        # mysql insert not support alias
        return self.statement.table_alias

    def get_original_sql(self):
        return self.original_sql

    def get_insert_columns(self):
        return self.statement.columns

    def get_insert_rows(self, pk_index: list):
        values_list = self.statement.values_list
        rows = []
        for i in range(len(values_list)):
            row = []
            values = values_list[i]
            for j in range(len(values)):
                value = values[j]
                if isinstance(value, MySQLValue.NullValue):
                    row.append(value)
                elif isinstance(value, MySQLValue.ValueExpr):
                    row.append(value.get_value())
                elif isinstance(value, MySQLValue.FunctionNameValue):
                    row.append(value)
                elif isinstance(value, MySQLValue.ParameterMarkerValue):
                    row.append(value)
                else:
                    if j in pk_index:
                        raise SQLParsingException(
                            "Unknown SQLExpr:" + str(value))
                    row.append(NotPlaceholderValue())
            rows.append(row)
        return rows

    def insert_columns_is_empty(self):
        insert_columns = self.get_insert_columns()
        return insert_columns is None or len(insert_columns) <= 0
