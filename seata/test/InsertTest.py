#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author jsbxyyx
# @since 1.0
import pymysql
from dbutils.pooled_db import PooledDB

from seata.Boostrap import Bootstrap
from seata.rm.RMClient import RMClient
from seata.rm.datasource.PooledDBProxy import PooledDBProxy
from seata.sqlparser.util.JdbcConstants import JdbcConstants
from seata.test import pool_config
from seata.tm.TMClient import TMClient
from seata.tm.api.GlobalTransaction import DefaultGlobalTransaction, GlobalTransactionRole


def get_pool():
    host = pool_config.host
    port = pool_config.port
    user = pool_config.user
    password = pool_config.password
    database = pool_config.database
    return PooledDB(creator=pymysql, host=host, port=port, user=user, password=password, database=database)


def bootstrap_init():
    host = "127.0.0.1"
    port = 8091

    tm_client = TMClient.get()
    tm_client.application_id = "test"
    tm_client.transaction_service_group = "my_test_tx_group"
    tm_client.init_client(host, port)

    rm_client = RMClient.get()
    rm_client.application_id = tm_client.application_id
    rm_client.transaction_service_group = tm_client.transaction_service_group
    rm_client.init_client(host, port)

    Bootstrap.start()


def test_insert():
    bootstrap_init()

    pool = get_pool()

    pool_proxy = PooledDBProxy(pool, JdbcConstants.MYSQL)

    cp = pool_proxy.connection()

    t = DefaultGlobalTransaction(None, None, GlobalTransactionRole.Launcher)
    t.begin()

    cp.bind(t.get_xid())

    cursor = cp.cursor()
    cursor.execute("insert into test(id, name) values(%s, %s)", (None, "name1"))
    cp.commit()
    t.commit()
    print("success")


def test_get_table_meta():
    pool = get_pool()
    con = pool.connection()
    cursor = con.cursor()
    schema = con._pool._kwargs['database']
    sql = 'select * from information_schema.columns where table_name = %s and table_schema = %s'
    cursor.execute(sql, ('test', schema))
    all = cursor.fetchall()
    for i in range(len(all)):
        r = all[i]
        print(r)
    pass


def test_get_low_case():
    pool = get_pool()
    con = pool.connection()
    cursor = con.cursor()
    sql = "select * from information_schema.global_variables WHERE variable_name = 'LOWER_CASE_TABLE_NAMES'"
    cursor.execute(sql)
    one = cursor.fetchone()
    print(one)
    pass


def test_insert_lastrowid():
    pool = get_pool()
    con = pool.connection()
    cursor = con.cursor()
    sql = "insert into test (id, name) values(null, 1), (null, 2)"
    cursor.execute(sql)
    con.commit()
    print(cursor.lastrowid)
    print(cursor.lastrowid)
    print(cursor.rowcount)
    print()


def test_IntegrityError():
    pool = get_pool()
    con = pool.connection()
    try:
        cursor = con.cursor()
        sql = "insert into test (id, name) values(1, 1)"
        cursor.execute(sql)
        con.commit()
    except Exception as e:
        print(e.__class__.mro())


if __name__ == '__main__':
    test_insert()
    # test_get_table_meta()
    # test_get_low_case()
    # test_insert_lastrowid()
    # test_IntegrityError()
    print()
