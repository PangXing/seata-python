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

from am.mysql_base import MySqlBase, MysqlOutputVisitor, MysqlStatementVisitor


def test_insert():
    sql = """
        insert ignore into test values(?,?);
        insert into test values(%s, %s);
        insert into test (id, name) values (?,?);
        insert into test value (null, 'null', null, true, '1', 1, 1.0, now(6), format(250500.5634, 2));
        """
    ss = MySqlBase.parserSQLStatement(sql)

    for idx in range(len(ss)):
        s = MysqlStatementVisitor().visit(ss[idx])

        output = list()
        MysqlOutputVisitor().visitInsertStatement(s, output)
        sql_string = ''.join(output)
        print(sql_string)

    pass


def test_delete():
    sql = """
       delete from test where id = ?;
       delete from test where id = 1;
       delete t from test t where t.id = ?;
       delete t from test t where t.id = 1;
       """
    ss = MySqlBase.parserSQLStatement(sql)

    for idx in range(len(ss)):
        s = MysqlStatementVisitor().visit(ss[idx])

        output = list()
        MysqlOutputVisitor().visitDeleteStatement(s, output)
        sql_string = ''.join(output)
        print(sql_string)

    pass


def test_update():
    sql = """
        update test set id = ?, name = ? where id = ?;
        update test set id = 1, name = ? where id = 1;
        update test set id = 1, name = '1' where id = 1;
        update test t set id = ?, name = ? where t.id = ?;
        update test t set t.id = ?, t.name = ? where t.id = ? and t.name = ?;
        update test t set t.id = ?, t.name = ? where t.id not in (?, 1);
        update test t set t.id = ?, t.name = ? where t.id is null;
        update test t set t.id = ?, t.name = ? where t.id > ?;
        update test t set t.id = ?, t.name = ? where t.id like '?';
        """
    ss = MySqlBase.parserSQLStatement(sql)

    for idx in range(len(ss)):
        s = MysqlStatementVisitor().visit(ss[idx])

        output = list()
        MysqlOutputVisitor().visitUpdateStatement(s, output)
        sql_string = ''.join(output)
        print(sql_string)

    pass


def test_select():
    sql = """
        select * from test t where t.id = ?;
        select id, name from test where id = ?;
        select id, name from test where id = 1;
        """

    ss = MySqlBase.parserSQLStatement(sql)

    for idx in range(len(ss)):
        s = MysqlStatementVisitor().visit(ss[idx])

        output = list()
        MysqlOutputVisitor().visitSelectStatement(s, output)
        sql_string = ''.join(output)
        print(sql_string)

    pass


if __name__ == '__main__':
    test_insert()
    test_delete()
    test_update()
    test_select()
