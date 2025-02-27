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

from loguru import logger

from seata.core.context.RootContext import RootContext
from seata.core.model.GlobalStatus import GlobalStatus
from seata.tm.DefaultTransactionManager import DefaultTransactionManager
from seata.tm.api.GlobalTransaction import GlobalTransaction
from seata.tm.api.GlobalTransactionRole import GlobalTransactionRole


class DefaultGlobalTransaction(GlobalTransaction):
    def __init__(self, xid=None, status=GlobalStatus.UnKnown, role=GlobalTransactionRole.Launcher):
        self.transaction_manager = DefaultTransactionManager()
        self.xid = xid
        self.status = status
        self.role = role

    def begin(self, timeout=60000, name="default"):
        if self.role != GlobalTransactionRole.Launcher:
            self.__assert_xid_not_null()
            logger.debug('ignore begin, involved in global transaction xid : [{}]'.format(self.xid))
            return
        self.__assert_xid_null()
        current_xid = RootContext.get_xid()
        if current_xid is not None:
            raise ValueError("Global transaction already exists, "
                             "can't begin a new global transaction, currentXid = {}".format(self.xid))
        self.xid = self.transaction_manager.begin(None, None, name, timeout)
        self.status = GlobalStatus.Begin
        RootContext.bind(self.xid)
        logger.info('begin new global transaction [{}]'.format(self.xid))

    def commit(self):
        if self.role == GlobalTransactionRole.Participant:
            logger.debug('ignore commit, involved in global transaction xid : [{}]'.format(self.xid))
            return
        self.__assert_xid_not_null()
        self.status = self.transaction_manager.commit(self.xid)
        logger.info('commit global transaction [{}] [{}]'.format(self.xid, self.status))

    def rollback(self):
        if self.role == GlobalTransactionRole.Participant:
            logger.debug('ignore rollback, involved in global transaction xid : [{}]'.format(self.xid))
            return
        self.__assert_xid_not_null()
        self.status = self.transaction_manager.rollback(self.xid)
        logger.info('rollback global transaction [{}] [{}]'.format(self.xid, self.status))

    def get_status(self):
        if self.xid is None:
            return GlobalStatus.UnKnown
        return self.transaction_manager.get_status(self.xid)

    def get_xid(self):
        return self.xid

    def global_report(self, global_status):
        self.__assert_xid_not_null()
        if global_status is None:
            raise ValueError('global status is null')
        self.status = self.transaction_manager.global_report(self.xid, global_status)
        logger.info('report global transaction [{}] [{}]'.format(self.xid, global_status))

    def __assert_xid_null(self):
        if self.xid is not None:
            raise ValueError('xid is not null [{}]'.format(self.xid))

    def __assert_xid_not_null(self):
        if self.xid is None:
            raise ValueError('xid is null')